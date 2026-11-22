
-- Initial Admin account
-- Replace the password hash with a real Werkzeug-generated hash
-- before using this account.

INSERT INTO users (
    full_name,
    email,
    password_hash
)
VALUES (
    'Admin User',
    'admin@licenseloop.com',
    'REPLACE_WITH_REAL_PASSWORD_HASH'
);


-- Vendors

INSERT INTO vendors (
    vendor_name,
    contact_email,
    contact_phone,
    website
)
VALUES
(
    'Microsoft',
    'support@microsoft.com',
    '18001025010',
    'https://www.microsoft.com'
),
(
    'Adobe',
    'support@adobe.com',
    '18001020000',
    'https://www.adobe.com'
),
(
    'Google',
    'support@google.com',
    '18002004615',
    'https://www.google.com'
);


-- Software

INSERT INTO software (
    software_name,
    description,
    category,
    vendor_id
)
VALUES
(
    'Microsoft 365',
    'Productivity and office applications',
    'Productivity',
    1
),
(
    'Adobe Photoshop',
    'Image editing and graphic design software',
    'Design',
    2
),
(
    'Google Workspace',
    'Cloud-based productivity and collaboration tools',
    'Productivity',
    3
);
