
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE vendors (
    vendor_id SERIAL PRIMARY KEY,
    vendor_name VARCHAR(100) UNIQUE NOT NULL,
    contact_email VARCHAR(150),
    contact_phone VARCHAR(20),
    website VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE software (
    software_id SERIAL PRIMARY KEY,
    software_name VARCHAR(150) NOT NULL,
    description TEXT,
    category VARCHAR(100),
    vendor_id INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_software_vendor
        FOREIGN KEY (vendor_id)
        REFERENCES vendors(vendor_id)
        ON DELETE RESTRICT,

    CONSTRAINT unique_software_vendor
        UNIQUE (software_name, vendor_id)
);


CREATE TABLE licenses (
    license_id SERIAL PRIMARY KEY,

    software_id INTEGER NOT NULL,
    created_by INTEGER NOT NULL,

    license_type VARCHAR(30) NOT NULL
        CHECK (license_type IN ('subscription', 'perpetual')),

    quantity INTEGER NOT NULL
        CHECK (quantity > 0),

    purchase_date DATE NOT NULL,
    expiry_date DATE NOT NULL,

    cost NUMERIC(10,2) NOT NULL
        CHECK (cost >= 0),

    currency VARCHAR(3) NOT NULL DEFAULT 'INR',

    status VARCHAR(20) NOT NULL DEFAULT 'active'
        CHECK (
            status IN (
                'active',
                'expired',
                'cancelled',
                'suspended'
            )
        ),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_license_software
        FOREIGN KEY (software_id)
        REFERENCES software(software_id)
        ON DELETE RESTRICT,

    CONSTRAINT fk_license_user
        FOREIGN KEY (created_by)
        REFERENCES users(user_id)
        ON DELETE RESTRICT,

    CONSTRAINT check_license_dates
        CHECK (expiry_date >= purchase_date)
);


-- Performance indexes

CREATE INDEX idx_software_vendor
ON software(vendor_id);

CREATE INDEX idx_license_software
ON licenses(software_id);

CREATE INDEX idx_license_created_by
ON licenses(created_by);

CREATE INDEX idx_license_expiry
ON licenses(expiry_date);

CREATE INDEX idx_license_status
ON licenses(status);
