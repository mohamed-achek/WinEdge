# WinEdge: Business Intelligence Project

## Overview
WinEdge is a comprehensive Business Intelligence (BI) project designed to analyze sales and inventory data to enable informed decision-making for a retail company. The project focuses on studying past performance (2019-2022) and providing actionable insights to guide strategic initiatives such as expanding into new territories, optimizing store performance, and improving inventory management.

---

## Key Features
- **Data Extraction**: Consolidates data from multiple sources (CSV files, SQL databases, MongoDB).
- **Data Transformation**: Cleans and processes raw data, ensuring consistency, removing duplicates, and assigning unique identifiers to customers.
- **Data Loading**: Loads the processed data into a PostgreSQL database for scalable and efficient querying.
- **Dashboards**: Provides interactive visualizations for decision-makers using Power BI.
- **Integration**: Seamlessly integrates with Python applications for real-time analysis and reporting.

---

## Tech Stack
- **Database**: PostgreSQL for robust storage and querying.
- **Programming**: Python for data handling, analysis, and application integration.
- **Data Sources**: CSV, SQL databases, MongoDB.
- **Visualization**: Power BI for dashboards and reports.

---

## ETL Process
1. **Extraction**: Data collected from CSV files, SQL databases, and MongoDB.
2. **Transformation**: Data cleaned to remove duplicates, ensure consistency, and assign unique identifiers.
3. **Loading**: Processed data stored in PostgreSQL for further analysis and visualization.

---

## Project Objectives
- Identify optimal areas for expansion and underperforming locations for closure or transfer.
- Analyze customer segments and target profitable demographics.
- Streamline inventory management to reduce waste and improve availability.
- Enable strategic decisions through actionable insights derived from data.

---

## Setup Instructions

1. Clone this repository:
   ```bash
   git clone https://github.com/mohamed-achek/WinEdge.git
   ```
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up the PostgreSQL database and update the connection details in the configuration file.
4. Run the ETL pipeline to process and load data into the database:
   ```bash
   python etl_pipeline.py
   ```
5. Launch the dashboard or Python application for analysis and visualization.

---

## Contributing
We welcome contributions to enhance the functionality of WinEdge. Please fork the repository, make your changes, and submit a pull request. Ensure your code adheres to the project's style and includes relevant documentation.

---

## Contact
For questions or feedback, please reach out to the project maintainers at:

- mohamedachek5@gmail.com
- mohamedaminesaoudi03@gmail.com
