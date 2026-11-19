INSERT INTO users (full_name, email, password_hash)
VALUES
('Admin User', 'admin@licenseloop.com', 'DEMO_HASH_1'),
('Rahul Sharma', 'rahul@example.com', 'DEMO_HASH_2'),
('Priya Patel', 'priya@example.com', 'DEMO_HASH_3');

INSERT INTO vendors (vendor_name, contact_email, contact_phone, website)
VALUES
('Microsoft', 'support@microsoft.com', '18001025010', 'https://www.microsoft.com'),
('Adobe', 'support@adobe.com', '18001020000', 'https://www.adobe.com'),
('Google', 'support@google.com', '18002004615', 'https://www.google.com');

INSERT INTO software (software_name, description, category, vendor_id)
VALUES
('Microsoft 365', 'Productivity and office applications', 'Productivity', 1),
('Adobe Photoshop', 'Image editing and graphic design software', 'Design', 2),
('Google Workspace', 'Cloud-based productivity and collaboration tools', 'Productivity', 3);

INSERT INTO licenses (
    software_id,
    created_by,
    license_type,
    quantity,
    purchase_date,
    expiry_date,
    cost,
    currency,
    status
)
VALUES
(1, 1, 'subscription', 50, '2026-01-01', '2027-01-01', 60000, 'INR', 'active'),
(2, 2, 'subscription', 10, '2026-02-01', '2026-12-10', 25000, 'INR', 'active'),
(3, 3, 'subscription', 30, '2025-01-01', '2026-10-01', 45000, 'INR', 'expired');


