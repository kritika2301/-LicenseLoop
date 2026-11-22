
import csv
import io

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    Response,
    session
)

from app.db import get_db_connection


main = Blueprint("main", __name__)


# ==========================================
# 1. DASHBOARD
# ==========================================

@main.route("/")
@main.route("/dashboard")
def dashboard():

    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            (SELECT COUNT(*) FROM software),

            (SELECT COUNT(*) FROM licenses),

            (SELECT COUNT(*)
             FROM licenses
             WHERE expiry_date >= CURRENT_DATE
             AND status = 'active'),

            (SELECT COUNT(*)
             FROM licenses
             WHERE expiry_date < CURRENT_DATE
             OR status = 'expired'),

            (SELECT COUNT(*)
             FROM licenses
             WHERE expiry_date BETWEEN CURRENT_DATE
             AND CURRENT_DATE + INTERVAL '30 days'
             AND status = 'active'),

            (SELECT COALESCE(SUM(cost), 0)
             FROM licenses);
    """)

    result = cursor.fetchone()

    stats = {
        "total_software": result[0],
        "total_licenses": result[1],
        "active_licenses": result[2],
        "expired_licenses": result[3],
        "expiring_soon": result[4],
        "total_expenditure": result[5]
    }

    cursor.execute("""
        SELECT
            s.software_name,
            v.vendor_name,
            l.license_type,
            l.expiry_date,

            CASE
                WHEN l.expiry_date < CURRENT_DATE
                     OR l.status = 'expired'
                    THEN 'expired'

                WHEN l.status = 'active'
                     AND l.expiry_date <= CURRENT_DATE
                         + INTERVAL '30 days'
                    THEN 'expiring soon'

                ELSE l.status
            END AS display_status

        FROM licenses l

        JOIN software s
            ON l.software_id = s.software_id

        JOIN vendors v
            ON s.vendor_id = v.vendor_id

        ORDER BY l.created_at DESC
        LIMIT 5;
    """)

    recent_licenses = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "dashboard.html",
        stats=stats,
        recent_licenses=recent_licenses
    )


# ==========================================
# 2. DATABASE TEST
# ==========================================

@main.route("/db-test")
def db_test():

    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT current_database();")

        database_name = cursor.fetchone()[0]

        cursor.close()
        connection.close()

        return f"Successfully connected to {database_name}!"

    except Exception as error:
        return f"Database connection failed: {error}", 500


# ==========================================
# 3. SOFTWARE MANAGEMENT
# ==========================================

@main.route("/software", methods=["GET", "POST"])
def software_list():

    connection = get_db_connection()
    cursor = connection.cursor()
    error = None

    if request.method == "POST":

        software_name = request.form.get(
            "software_name", ""
        ).strip()

        description = request.form.get(
            "description", ""
        ).strip()

        category = request.form.get(
            "category", ""
        ).strip()

        vendor_id = request.form.get("vendor_id", "")

        try:

            if not software_name or not vendor_id:
                raise ValueError(
                    "Software name and vendor are required."
                )

            cursor.execute("""
                INSERT INTO software
                    (software_name, description, category, vendor_id)
                VALUES (%s, %s, %s, %s);
            """, (
                software_name,
                description or None,
                category or None,
                int(vendor_id)
            ))

            connection.commit()

            cursor.close()
            connection.close()

            return redirect(url_for("main.software_list"))

        except Exception as e:
            connection.rollback()
            error = str(e)

    search = request.args.get("search", "").strip()

    selected_category = request.args.get(
        "category", ""
    ).strip()

    selected_vendor = request.args.get(
        "vendor", ""
    ).strip()

    query = """
        SELECT
            s.software_id,
            s.software_name,
            s.description,
            s.category,
            v.vendor_name

        FROM software s

        JOIN vendors v
            ON s.vendor_id = v.vendor_id

        WHERE 1=1
    """

    parameters = []

    if search:
        query += " AND s.software_name ILIKE %s "
        parameters.append(f"%{search}%")

    if selected_category:
        query += " AND s.category = %s "
        parameters.append(selected_category)

    if selected_vendor:
        try:
            query += " AND s.vendor_id = %s "
            parameters.append(int(selected_vendor))
        except ValueError:
            selected_vendor = ""

    query += " ORDER BY s.software_id DESC;"

    cursor.execute(query, parameters)

    software = cursor.fetchall()

    cursor.execute("""
        SELECT vendor_id, vendor_name
        FROM vendors
        ORDER BY vendor_name;
    """)

    vendors = cursor.fetchall()

    cursor.execute("""
        SELECT DISTINCT category
        FROM software
        WHERE category IS NOT NULL
        ORDER BY category;
    """)

    categories = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "software.html",
        software=software,
        vendors=vendors,
        categories=categories,
        search=search,
        selected_category=selected_category,
        selected_vendor=selected_vendor,
        error=error
    )


# Edit software

@main.route(
    "/software/edit/<int:software_id>",
    methods=["GET", "POST"]
)
def edit_software(software_id):

    connection = get_db_connection()
    cursor = connection.cursor()
    error = None

    if request.method == "POST":

        software_name = request.form.get(
            "software_name", ""
        ).strip()

        description = request.form.get(
            "description", ""
        ).strip()

        category = request.form.get(
            "category", ""
        ).strip()

        vendor_id = request.form.get("vendor_id", "")

        try:

            if not software_name or not vendor_id:
                raise ValueError(
                    "Software name and vendor are required."
                )

            cursor.execute("""
                UPDATE software
                SET software_name = %s,
                    description = %s,
                    category = %s,
                    vendor_id = %s
                WHERE software_id = %s;
            """, (
                software_name,
                description or None,
                category or None,
                int(vendor_id),
                software_id
            ))

            if cursor.rowcount == 0:
                raise ValueError("Software record not found.")

            connection.commit()

            cursor.close()
            connection.close()

            return redirect(url_for("main.software_list"))

        except Exception as e:
            connection.rollback()
            error = str(e)

    cursor.execute("""
        SELECT
            software_id,
            software_name,
            description,
            category,
            vendor_id

        FROM software
        WHERE software_id = %s;
    """, (software_id,))

    software = cursor.fetchone()

    if software is None:

        cursor.close()
        connection.close()

        return "Software record not found.", 404

    cursor.execute("""
        SELECT vendor_id, vendor_name
        FROM vendors
        ORDER BY vendor_name;
    """)

    vendors = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "edit_software.html",
        software=software,
        vendors=vendors,
        error=error
    )


# Delete software

@main.route(
    "/software/delete/<int:software_id>",
    methods=["POST"]
)
def delete_software(software_id):

    connection = get_db_connection()
    cursor = connection.cursor()

    try:

        cursor.execute("""
            DELETE FROM software
            WHERE software_id = %s;
        """, (software_id,))

        if cursor.rowcount == 0:

            connection.rollback()

            cursor.close()
            connection.close()

            return "Software record not found.", 404

        connection.commit()

    except Exception:

        connection.rollback()

        cursor.close()
        connection.close()

        return (
            "Cannot delete this software because it may be "
            "associated with existing licenses.",
            409
        )

    cursor.close()
    connection.close()

    return redirect(url_for("main.software_list"))


# ==========================================
# 4. VENDOR MANAGEMENT
# ==========================================

@main.route("/vendors", methods=["GET", "POST"])
def vendors_list():

    connection = get_db_connection()
    cursor = connection.cursor()
    error = None

    if request.method == "POST":

        vendor_name = request.form.get(
            "vendor_name", ""
        ).strip()

        contact_email = request.form.get(
            "contact_email", ""
        ).strip()

        contact_phone = request.form.get(
            "contact_phone", ""
        ).strip()

        website = request.form.get(
            "website", ""
        ).strip()

        try:

            if not vendor_name:
                raise ValueError("Vendor name is required.")

            cursor.execute("""
                INSERT INTO vendors
                    (vendor_name, contact_email,
                     contact_phone, website)

                VALUES (%s, %s, %s, %s);
            """, (
                vendor_name,
                contact_email or None,
                contact_phone or None,
                website or None
            ))

            connection.commit()

            cursor.close()
            connection.close()

            return redirect(url_for("main.vendors_list"))

        except Exception as e:
            connection.rollback()
            error = str(e)

    search = request.args.get("search", "").strip()

    query = """
        SELECT
            vendor_id,
            vendor_name,
            contact_email,
            contact_phone,
            website

        FROM vendors
        WHERE 1=1
    """

    parameters = []

    if search:
        query += " AND vendor_name ILIKE %s "
        parameters.append(f"%{search}%")

    query += " ORDER BY vendor_id DESC;"

    cursor.execute(query, parameters)

    vendors = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "vendors.html",
        vendors=vendors,
        search=search,
        error=error
    )


# Edit vendor

@main.route(
    "/vendors/edit/<int:vendor_id>",
    methods=["GET", "POST"]
)
def edit_vendor(vendor_id):

    connection = get_db_connection()
    cursor = connection.cursor()
    error = None

    if request.method == "POST":

        vendor_name = request.form.get(
            "vendor_name", ""
        ).strip()

        contact_email = request.form.get(
            "contact_email", ""
        ).strip()

        contact_phone = request.form.get(
            "contact_phone", ""
        ).strip()

        website = request.form.get(
            "website", ""
        ).strip()

        try:

            if not vendor_name:
                raise ValueError("Vendor name is required.")

            cursor.execute("""
                UPDATE vendors
                SET vendor_name = %s,
                    contact_email = %s,
                    contact_phone = %s,
                    website = %s

                WHERE vendor_id = %s;
            """, (
                vendor_name,
                contact_email or None,
                contact_phone or None,
                website or None,
                vendor_id
            ))

            if cursor.rowcount == 0:
                raise ValueError("Vendor not found.")

            connection.commit()

            cursor.close()
            connection.close()

            return redirect(url_for("main.vendors_list"))

        except Exception as e:
            connection.rollback()
            error = str(e)

    cursor.execute("""
        SELECT
            vendor_id,
            vendor_name,
            contact_email,
            contact_phone,
            website

        FROM vendors
        WHERE vendor_id = %s;
    """, (vendor_id,))

    vendor = cursor.fetchone()

    if vendor is None:

        cursor.close()
        connection.close()

        return "Vendor not found.", 404

    cursor.close()
    connection.close()

    return render_template(
        "edit_vendor.html",
        vendor=vendor,
        error=error
    )


# Delete vendor

@main.route(
    "/vendors/delete/<int:vendor_id>",
    methods=["POST"]
)
def delete_vendor(vendor_id):

    connection = get_db_connection()
    cursor = connection.cursor()

    try:

        cursor.execute("""
            DELETE FROM vendors
            WHERE vendor_id = %s;
        """, (vendor_id,))

        if cursor.rowcount == 0:

            connection.rollback()

            cursor.close()
            connection.close()

            return "Vendor not found.", 404

        connection.commit()

    except Exception:

        connection.rollback()

        cursor.close()
        connection.close()

        return (
            "Cannot delete this vendor because it is associated "
            "with existing software. Delete or reassign that software first.",
            409
        )

    cursor.close()
    connection.close()

    return redirect(url_for("main.vendors_list"))

# ==========================================
# 5. LICENSE MANAGEMENT
# ==========================================

@main.route("/licenses", methods=["GET", "POST"])
def licenses_list():

    connection = get_db_connection()
    cursor = connection.cursor()
    error = None

    # Add license

    if request.method == "POST":

        try:

            software_id = int(
                request.form.get("software_id", "")
            )

            license_type = request.form.get(
                "license_type", ""
            )

            quantity = int(
                request.form.get("quantity", "")
            )

            purchase_date = request.form.get(
                "purchase_date", ""
            )

            expiry_date = request.form.get(
                "expiry_date", ""
            )

            cost = request.form.get("cost", "")

            currency = request.form.get(
                "currency", "INR"
            )

            status = request.form.get(
                "status", "active"
            )

            if license_type not in (
                "subscription", "perpetual"
            ):
                raise ValueError("Select a valid license type.")

            if quantity <= 0:
                raise ValueError(
                    "Quantity must be greater than zero."
                )

            if not purchase_date or not expiry_date:
                raise ValueError(
                    "Both dates are required."
                )

            if expiry_date < purchase_date:
                raise ValueError(
                    "Expiry date cannot be before purchase date."
                )

            if status not in (
                "active", "expired", "cancelled", "suspended"
            ):
                raise ValueError("Select a valid license status.")

            if currency not in (
                "INR", "USD", "EUR", "GBP"
            ):
                raise ValueError("Select a valid currency.")

            cursor.execute("""
                INSERT INTO licenses
                    (software_id, created_by, license_type,
                     quantity, purchase_date, expiry_date,
                     cost, currency, status)

                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
            """, (
                software_id,
                session["user_id"],
                license_type,
                quantity,
                purchase_date,
                expiry_date,
                cost,
                currency,
                status
            ))

            connection.commit()

            cursor.close()
            connection.close()

            return redirect(url_for("main.licenses_list"))

        except Exception as e:
            connection.rollback()
            error = str(e)

    # Search and filters

    search = request.args.get("search", "").strip()

    selected_vendor = request.args.get(
        "vendor", ""
    ).strip()

    selected_status = request.args.get(
        "status", ""
    ).strip()

    query = """
        SELECT
            l.license_id,
            s.software_name,
            v.vendor_name,
            l.license_type,
            l.quantity,
            l.purchase_date,
            l.expiry_date,
            l.cost,
            l.currency,
            l.status

        FROM licenses l

        JOIN software s
            ON l.software_id = s.software_id

        JOIN vendors v
            ON s.vendor_id = v.vendor_id

        WHERE 1=1
    """

    parameters = []

    if search:
        query += " AND s.software_name ILIKE %s "
        parameters.append(f"%{search}%")

    if selected_vendor:

        try:
            query += " AND v.vendor_id = %s "
            parameters.append(int(selected_vendor))

        except ValueError:
            selected_vendor = ""

    if selected_status in (
        "active", "expired", "cancelled", "suspended"
    ):

        query += " AND l.status = %s "
        parameters.append(selected_status)

    elif selected_status:
        selected_status = ""

    query += " ORDER BY l.license_id DESC;"

    cursor.execute(query, parameters)

    licenses = cursor.fetchall()

    # Software dropdown

    cursor.execute("""
        SELECT
            s.software_id,
            s.software_name,
            v.vendor_name

        FROM software s

        JOIN vendors v
            ON s.vendor_id = v.vendor_id

        ORDER BY s.software_name;
    """)

    software_options = cursor.fetchall()

    # Vendor dropdown

    cursor.execute("""
        SELECT vendor_id, vendor_name
        FROM vendors
        ORDER BY vendor_name;
    """)

    vendors = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "licenses.html",
        licenses=licenses,
        software_options=software_options,
        vendors=vendors,
        search=search,
        selected_vendor=selected_vendor,
        selected_status=selected_status,
        error=error
    )


# Edit license

@main.route(
    "/licenses/edit/<int:license_id>",
    methods=["GET", "POST"]
)
def edit_license(license_id):

    connection = get_db_connection()
    cursor = connection.cursor()
    error = None

    if request.method == "POST":

        try:

            software_id = int(
                request.form.get("software_id", "")
            )

            license_type = request.form.get(
                "license_type", ""
            )

            quantity = int(
                request.form.get("quantity", "")
            )

            purchase_date = request.form.get(
                "purchase_date", ""
            )

            expiry_date = request.form.get(
                "expiry_date", ""
            )

            cost = request.form.get("cost", "")

            currency = request.form.get(
                "currency", "INR"
            )

            status = request.form.get(
                "status", "active"
            )

            if license_type not in (
                "subscription", "perpetual"
            ):
                raise ValueError("Select a valid license type.")

            if quantity <= 0:
                raise ValueError(
                    "Quantity must be greater than zero."
                )

            if not purchase_date or not expiry_date:
                raise ValueError("Both dates are required.")

            if expiry_date < purchase_date:
                raise ValueError(
                    "Expiry date cannot be before purchase date."
                )

            if status not in (
                "active", "expired", "cancelled", "suspended"
            ):
                raise ValueError("Select a valid license status.")

            if currency not in (
                "INR", "USD", "EUR", "GBP"
            ):
                raise ValueError("Select a valid currency.")

            cursor.execute("""
                UPDATE licenses

                SET software_id = %s,
                    license_type = %s,
                    quantity = %s,
                    purchase_date = %s,
                    expiry_date = %s,
                    cost = %s,
                    currency = %s,
                    status = %s

                WHERE license_id = %s;
            """, (
                software_id,
                license_type,
                quantity,
                purchase_date,
                expiry_date,
                cost,
                currency,
                status,
                license_id
            ))

            if cursor.rowcount == 0:
                raise ValueError("License record not found.")

            connection.commit()

            cursor.close()
            connection.close()

            return redirect(url_for("main.licenses_list"))

        except Exception as e:
            connection.rollback()
            error = str(e)

    cursor.execute("""
        SELECT
            license_id,
            software_id,
            license_type,
            quantity,
            purchase_date,
            expiry_date,
            cost,
            currency,
            status

        FROM licenses
        WHERE license_id = %s;
    """, (license_id,))

    license_record = cursor.fetchone()

    if license_record is None:

        cursor.close()
        connection.close()

        return "License record not found.", 404

    cursor.execute("""
        SELECT
            s.software_id,
            s.software_name,
            v.vendor_name

        FROM software s

        JOIN vendors v
            ON s.vendor_id = v.vendor_id

        ORDER BY s.software_name;
    """)

    software_options = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "edit_license.html",
        license=license_record,
        software_options=software_options,
        error=error
    )


# Delete license

@main.route(
    "/licenses/delete/<int:license_id>",
    methods=["POST"]
)
def delete_license(license_id):

    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("""
        DELETE FROM licenses
        WHERE license_id = %s;
    """, (license_id,))

    if cursor.rowcount == 0:

        connection.rollback()

        cursor.close()
        connection.close()

        return "License not found.", 404

    connection.commit()

    cursor.close()
    connection.close()

    return redirect(url_for("main.licenses_list"))


# ==========================================
# 6. RENEWAL TRACKING
# ==========================================

@main.route("/renewals")
def renewals():

    connection = get_db_connection()
    cursor = connection.cursor()

    # Automatically mark past-due active licenses as expired

    cursor.execute("""
        UPDATE licenses
        SET status = 'expired'
        WHERE expiry_date < CURRENT_DATE
        AND status = 'active';
    """)

    connection.commit()

    # Fetch upcoming and expired renewals

    cursor.execute("""
        SELECT
            l.license_id,
            s.software_name,
            v.vendor_name,
            l.license_type,
            l.expiry_date,
            l.cost,
            l.currency,
            l.status,

            (l.expiry_date - CURRENT_DATE)
                AS days_remaining

        FROM licenses l

        JOIN software s
            ON l.software_id = s.software_id

        JOIN vendors v
            ON s.vendor_id = v.vendor_id

        WHERE l.expiry_date <= CURRENT_DATE
              + INTERVAL '30 days'

        AND l.status NOT IN ('cancelled', 'suspended')

        ORDER BY l.expiry_date ASC;
    """)

    renewal_records = cursor.fetchall()

    # Renewal summary

    cursor.execute("""
        SELECT

            COUNT(*) FILTER (
                WHERE expiry_date < CURRENT_DATE
                OR status = 'expired'
            ),

            COUNT(*) FILTER (
                WHERE status = 'active'
                AND expiry_date BETWEEN CURRENT_DATE
                AND CURRENT_DATE + INTERVAL '7 days'
            ),

            COUNT(*) FILTER (
                WHERE status = 'active'
                AND expiry_date > CURRENT_DATE + INTERVAL '7 days'
                AND expiry_date <= CURRENT_DATE + INTERVAL '30 days'
            )

        FROM licenses

        WHERE status NOT IN ('cancelled', 'suspended');
    """)

    summary_result = cursor.fetchone()

    renewal_summary = {
        "expired": summary_result[0],
        "due_this_week": summary_result[1],
        "due_this_month": summary_result[2]
    }

    cursor.close()
    connection.close()

    return render_template(
        "renewals.html",
        renewal_records=renewal_records,
        renewal_summary=renewal_summary
    )


# Update renewal status

@main.route(
    "/renewals/update/<int:license_id>",
    methods=["POST"]
)
def update_renewal_status(license_id):

    status = request.form.get("status", "")

    if status not in (
        "active", "expired", "suspended", "cancelled"
    ):
        return "Invalid license status.", 400

    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE licenses
        SET status = %s
        WHERE license_id = %s;
    """, (status, license_id))

    if cursor.rowcount == 0:

        connection.rollback()

        cursor.close()
        connection.close()

        return "License not found.", 404

    connection.commit()

    cursor.close()
    connection.close()

    return redirect(url_for("main.renewals"))


# ==========================================
# 7. REPORTS AND ANALYTICS
# ==========================================

@main.route("/reports")
def reports():

    connection = get_db_connection()
    cursor = connection.cursor()

    # License summary

    cursor.execute("""
        SELECT
            COUNT(*),

            COUNT(*) FILTER (
                WHERE status = 'active'
                AND expiry_date > CURRENT_DATE + INTERVAL '30 days'
            ),

            COUNT(*) FILTER (
                WHERE expiry_date < CURRENT_DATE
                OR status = 'expired'
            ),

            COUNT(*) FILTER (
                WHERE status = 'active'
                AND expiry_date BETWEEN CURRENT_DATE
                AND CURRENT_DATE + INTERVAL '30 days'
            )

        FROM licenses;
    """)

    result = cursor.fetchone()

    summary = {
        "total": result[0],
        "active": result[1],
        "expired": result[2],
        "expiring": result[3]
    }

    # License status report

    cursor.execute("""
        SELECT
            CASE
                WHEN expiry_date < CURRENT_DATE
                     OR status = 'expired'
                    THEN 'Expired'

                WHEN status = 'active'
                     AND expiry_date <= CURRENT_DATE
                         + INTERVAL '30 days'
                    THEN 'Expiring Soon'

                WHEN status = 'active'
                    THEN 'Active'

                WHEN status = 'suspended'
                    THEN 'Suspended'

                ELSE 'Cancelled'
            END AS display_status,

            COUNT(*)

        FROM licenses

        GROUP BY display_status

        ORDER BY display_status;
    """)

    status_data = cursor.fetchall()

    # Upcoming and expired renewal report

    cursor.execute("""
        SELECT
            s.software_name,
            v.vendor_name,
            l.license_type,
            l.expiry_date,
            (l.expiry_date - CURRENT_DATE) AS days_remaining

        FROM licenses l

        JOIN software s
            ON l.software_id = s.software_id

        JOIN vendors v
            ON s.vendor_id = v.vendor_id

        WHERE l.expiry_date <= CURRENT_DATE
              + INTERVAL '30 days'

        AND l.status NOT IN ('cancelled', 'suspended')

        ORDER BY l.expiry_date ASC;
    """)

    renewal_data = cursor.fetchall()

    # Software expenditure report

    cursor.execute("""
        SELECT
            s.software_name,
            v.vendor_name,
            l.currency,
            SUM(l.cost) AS total_expenditure,
            COUNT(l.license_id) AS license_count

        FROM licenses l

        JOIN software s
            ON l.software_id = s.software_id

        JOIN vendors v
            ON s.vendor_id = v.vendor_id

        GROUP BY
            s.software_name,
            v.vendor_name,
            l.currency

        ORDER BY total_expenditure DESC;
    """)

    expenditure_data = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "reports.html",
        summary=summary,
        status_data=status_data,
        renewal_data=renewal_data,
        expenditure_data=expenditure_data
    )


# ==========================================
# 8. EXPORT REPORTS TO CSV
# ==========================================

@main.route("/reports/export")
def export_reports_csv():

    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            l.license_id,
            s.software_name,
            v.vendor_name,
            l.license_type,
            l.quantity,
            l.purchase_date,
            l.expiry_date,
            l.cost,
            l.currency,

            CASE
                WHEN l.expiry_date < CURRENT_DATE
                     OR l.status = 'expired'
                    THEN 'Expired'

                WHEN l.status = 'active'
                     AND l.expiry_date <= CURRENT_DATE
                         + INTERVAL '30 days'
                    THEN 'Expiring Soon'

                ELSE INITCAP(l.status)
            END AS display_status

        FROM licenses l

        JOIN software s
            ON l.software_id = s.software_id

        JOIN vendors v
            ON s.vendor_id = v.vendor_id

        ORDER BY l.license_id;
    """)

    records = cursor.fetchall()

    cursor.close()
    connection.close()

    output = io.StringIO()

    writer = csv.writer(output)

    writer.writerow([
        "License ID",
        "Software",
        "Vendor",
        "License Type",
        "Quantity",
        "Purchase Date",
        "Expiry Date",
        "Cost",
        "Currency",
        "Status"
    ])

    for record in records:
        writer.writerow(record)

    response = Response(
        output.getvalue(),
        mimetype="text/csv"
    )

    response.headers["Content-Disposition"] = (
        "attachment; filename=LicenseLoop_Reports.csv"
    )

    return response
