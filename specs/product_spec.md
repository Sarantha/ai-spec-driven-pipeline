# Feature Specification

## Feature Objective

Enhance the CSV processing application to extract both unique customer IDs and unique product IDs from the input dataset and generate separate output files.

---

## User Story

**As a** system operator,  
**I want** the application to extract unique customer IDs and unique product IDs into separate CSV files,  
**So that** downstream systems can independently process customer and product datasets.

---

## Business Rules

- The input CSV file must contain both `customer_id` and `product_id` columns.
- A `customer_id` may appear multiple times across different product associations.
- A `product_id` may appear multiple times across different customer associations.
- The system must extract only distinct `customer_id` values.
- The system must extract only distinct `product_id` values.
- The customer output file must contain a single `customer_id` column.
- The product output file must contain a single `product_id` column.
- The generated output files must be saved in the `output` directory.

---

## Acceptance Criteria

1. The application must read an input CSV file from the `input` directory.
2. The system must generate `unique_customers.csv` containing only unique customer IDs.
3. The system must generate `unique_products.csv` containing only unique product IDs.
4. The customer output CSV must contain a `customer_id` header.
5. The product output CSV must contain a `product_id` header.
6. Duplicate `customer_id` values must not appear in the customer output file.
7. Duplicate `product_id` values must not appear in the product output file.
8. The application must follow OOP design principles with separated service responsibilities.

---

## Non-Functional Requirements

- The implementation must maintain PEP8 compliance.
- The application should follow SOLID design principles.
- The codebase should separate business logic from file processing responsibilities.
- The application should remain modular and easily extensible for future entity extraction requirements.

---

## Out of Scope

- Database persistence support.
- REST API integration.
- Real-time streaming file processing.
- Handling encrypted or compressed CSV files.