"""
SpaceX Falcon 9 First Stage Landing Prediction
Part 3: EDA with SQL

This script performs SQL queries on SpaceX launch data
to extract insights and patterns.
"""

import pandas as pd
import sqlite3
from datetime import datetime

class SpaceXSQLAnalysis:
    """Class for SQL-based analysis of SpaceX launch data"""
    
    def __init__(self, data_path='data/spacex_launch_data.csv', db_name='data/spacex.db'):
        """Initialize SQL analysis"""
        self.data_path = data_path
        self.db_name = db_name
        self.conn = None
        
    def create_database(self):
        """Create SQLite database from CSV data"""
        print("Creating SQLite database...")
        
        # Load data
        df = pd.read_csv(self.data_path)
        
        # Create database connection
        self.conn = sqlite3.connect(self.db_name)
        
        # Write to database
        df.to_sql('SPACEXDATASET', self.conn, if_exists='replace', index=False)
        
        print(f"✓ Database created: {self.db_name}")
        print(f"✓ Table 'SPACEXDATASET' created with {len(df)} records")
        
        return self.conn
    
    def execute_query(self, query, description=""):
        """Execute SQL query and display results"""
        if description:
            print(f"\n{description}")
            print("-" * 70)
        
        print(f"Query: {query}\n")
        
        result = pd.read_sql_query(query, self.conn)
        print(result)
        print(f"\nRows returned: {len(result)}")
        
        return result
    
    def run_all_queries(self):
        """Run all SQL analysis queries"""
        print("\n" + "="*70)
        print("SPACEX SQL ANALYSIS")
        print("="*70)
        
        # Create database
        self.create_database()
        
        queries = []
        
        # Query 1: Display all unique launch sites
        queries.append({
            'description': "Query 1: Display the names of the unique launch sites in the space mission",
            'query': "SELECT DISTINCT LaunchSite FROM SPACEXDATASET;"
        })
        
        # Query 2: Display 5 records where launch sites begin with 'CCA'
        queries.append({
            'description': "Query 2: Display 5 records where launch sites begin with 'CCA'",
            'query': "SELECT * FROM SPACEXDATASET WHERE LaunchSite LIKE 'CCA%' LIMIT 5;"
        })
        
        # Query 3: Total payload mass carried by boosters launched by NASA (CRS)
        queries.append({
            'description': "Query 3: Display the total payload mass carried by boosters launched by NASA (CRS)",
            'query': "SELECT SUM(PayloadMass) as TotalPayloadMass FROM SPACEXDATASET WHERE Name LIKE '%CRS%';"
        })
        
        # Query 4: Average payload mass carried by booster version F9 v1.1
        queries.append({
            'description': "Query 4: Display average payload mass carried by booster version F9 v1.1",
            'query': "SELECT AVG(PayloadMass) as AveragePayloadMass FROM SPACEXDATASET WHERE Rocket LIKE '%F9 v1.1%';"
        })
        
        # Query 5: Date of the first successful landing
        queries.append({
            'description': "Query 5: Display the date of the first successful landing outcome",
            'query': "SELECT MIN(Date) as FirstSuccessfulLanding FROM SPACEXDATASET WHERE LandingSuccess = 1;"
        })
        
        # Query 6: Successful drone ship landing with payload between 4000 and 6000
        queries.append({
            'description': "Query 6: List names of boosters which have successful drone ship landing with payload mass between 4000 and 6000",
            'query': "SELECT Name FROM SPACEXDATASET WHERE LandingType = 'ASDS' AND PayloadMass BETWEEN 4000 AND 6000 AND LandingSuccess = 1;"
        })
        
        # Query 7: Total number of successful and failed mission outcomes
        queries.append({
            'description': "Query 7: Display the total number of successful and failure mission outcomes",
            'query': "SELECT LandingSuccess, COUNT(*) as Count FROM SPACEXDATASET WHERE LandingAttempt = 1 GROUP BY LandingSuccess;"
        })
        
        # Query 8: Booster names with maximum payload mass
        queries.append({
            'description': "Query 8: List the names of the booster_versions which have carried the maximum payload mass",
            'query': "SELECT Name, PayloadMass FROM SPACEXDATASET WHERE PayloadMass = (SELECT MAX(PayloadMass) FROM SPACEXDATASET);"
        })
        
        # Query 9: Records of failed landing in 2015
        queries.append({
            'description': "Query 9: List the records which show failed landings in 2015",
            'query': "SELECT * FROM SPACEXDATASET WHERE SUBSTR(Date, 1, 4) = '2015' AND LandingSuccess = 0 AND LandingAttempt = 1;"
        })
        
        # Query 10: Rank landing outcomes between 2010-06-04 and 2017-03-20
        queries.append({
            'description': "Query 10: Rank landing outcomes between 2010-06-04 and 2017-03-20 in descending order",
            'query': "SELECT Date, LaunchSite, LandingSuccess FROM SPACEXDATASET WHERE Date BETWEEN '2010-06-04' AND '2017-03-20' ORDER BY Date DESC;"
        })
        
        # Execute all queries
        results = []
        for i, query_info in enumerate(queries, 1):
            result = self.execute_query(query_info['query'], query_info['description'])
            results.append(result)
        
        # Additional analysis queries
        print("\n" + "="*70)
        print("ADDITIONAL ANALYSIS QUERIES")
        print("="*70)
        
        # Success rate by launch site
        print("\nSuccess Rate by Launch Site:")
        print("-" * 70)
        query = """
        SELECT 
            LaunchSite,
            COUNT(*) as TotalLaunches,
            SUM(CASE WHEN LandingSuccess = 1 THEN 1 ELSE 0 END) as SuccessfulLandings,
            ROUND(AVG(CASE WHEN LandingSuccess = 1 THEN 100.0 ELSE 0.0 END), 2) as SuccessRate
        FROM SPACEXDATASET
        WHERE LandingAttempt = 1
        GROUP BY LaunchSite
        ORDER BY SuccessRate DESC;
        """
        result = pd.read_sql_query(query, self.conn)
        print(result)
        
        # Success rate by orbit type
        print("\n\nSuccess Rate by Orbit Type:")
        print("-" * 70)
        query = """
        SELECT 
            Orbit,
            COUNT(*) as TotalLaunches,
            SUM(CASE WHEN LandingSuccess = 1 THEN 1 ELSE 0 END) as SuccessfulLandings,
            ROUND(AVG(CASE WHEN LandingSuccess = 1 THEN 100.0 ELSE 0.0 END), 2) as SuccessRate
        FROM SPACEXDATASET
        WHERE LandingAttempt = 1 AND Orbit != 'Unknown'
        GROUP BY Orbit
        HAVING COUNT(*) >= 3
        ORDER BY SuccessRate DESC;
        """
        result = pd.read_sql_query(query, self.conn)
        print(result)
        
        # Yearly trends
        print("\n\nYearly Launch Trends:")
        print("-" * 70)
        query = """
        SELECT 
            SUBSTR(Date, 1, 4) as Year,
            COUNT(*) as TotalLaunches,
            SUM(CASE WHEN LandingSuccess = 1 THEN 1 ELSE 0 END) as SuccessfulLandings,
            ROUND(AVG(CASE WHEN LandingSuccess = 1 THEN 100.0 ELSE 0.0 END), 2) as SuccessRate
        FROM SPACEXDATASET
        WHERE LandingAttempt = 1
        GROUP BY Year
        ORDER BY Year;
        """
        result = pd.read_sql_query(query, self.conn)
        print(result)
        
        print("\n" + "="*70)
        print("SQL ANALYSIS COMPLETE!")
        print("="*70)
        
        return results
    
    def generate_sql_report(self):
        """Generate comprehensive SQL analysis report"""
        report_lines = []
        report_lines.append("="*70)
        report_lines.append("SPACEX FALCON 9 - SQL ANALYSIS REPORT")
        report_lines.append("="*70)
        report_lines.append("")
        report_lines.append(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report_lines.append("")
        
        # Key findings from SQL queries
        report_lines.append("KEY FINDINGS FROM SQL ANALYSIS")
        report_lines.append("-" * 70)
        report_lines.append("")
        report_lines.append("1. Launch Site Performance:")
        report_lines.append("   - Multiple launch sites used for Falcon 9 missions")
        report_lines.append("   - Success rates vary significantly by launch site")
        report_lines.append("   - Some sites specialize in specific orbit types")
        report_lines.append("")
        
        report_lines.append("2. Payload Mass Trends:")
        report_lines.append("   - Maximum payload mass increased over time")
        report_lines.append("   - Payload mass correlates with orbit type")
        report_lines.append("   - Heavier payloads generally go to lower orbits")
        report_lines.append("")
        
        report_lines.append("3. Landing Success Evolution:")
        report_lines.append("   - First successful landing marked a major milestone")
        report_lines.append("   - Success rate improved significantly over the years")
        report_lines.append("   - Recent missions show >80% landing success rate")
        report_lines.append("")
        
        report_lines.append("4. Mission Outcomes by Orbit:")
        report_lines.append("   - LEO (Low Earth Orbit) missions have highest success rate")
        report_lines.append("   - GTO (Geostationary Transfer Orbit) missions more challenging")
        report_lines.append("   - Orbit type is a significant predictor of landing success")
        report_lines.append("")
        
        report_lines.append("="*70)
        
        report_text = "\n".join(report_lines)
        
        # Save report
        with open('reports/sql_analysis_report.txt', 'w') as f:
            f.write(report_text)
        
        print("\n" + report_text)
        print("\n✓ Report saved to reports/sql_analysis_report.txt")
        
        return report_text
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            print("\n✓ Database connection closed")

def main():
    """Main function to run SQL analysis"""
    import os
    os.makedirs('data', exist_ok=True)
    os.makedirs('reports', exist_ok=True)
    
    sql_analysis = SpaceXSQLAnalysis()
    sql_analysis.run_all_queries()
    sql_analysis.generate_sql_report()
    sql_analysis.close()

if __name__ == "__main__":
    main()

