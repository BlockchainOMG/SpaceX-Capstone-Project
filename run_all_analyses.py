"""
Master script to run all SpaceX Falcon 9 analyses
"""

import os
import sys

def run_analysis(script_name, description):
    """Run an analysis script"""
    print("\n" + "="*80)
    print(f"RUNNING: {description}")
    print("="*80)
    
    try:
        exec(open(script_name).read())
        print(f"\n✓ {description} completed successfully")
        return True
    except Exception as e:
        print(f"\n✗ Error in {description}: {str(e)}")
        return False

def main():
    """Run all analyses in sequence"""
    print("\n" + "="*80)
    print("SPACEX FALCON 9 CAPSTONE PROJECT - RUNNING ALL ANALYSES")
    print("="*80)
    
    analyses = [
        ('generate_sample_data.py', 'Data Generation'),
        ('spacex_data_collection.py', 'Data Collection (API)'),
        ('spacex_eda_visualization.py', 'Exploratory Data Analysis'),
        ('spacex_sql_analysis.py', 'SQL Analysis'),
        ('spacex_folium_map.py', 'Folium Interactive Maps'),
        ('spacex_dash_app.py', 'Plotly Dash Dashboard'),
        ('spacex_ml_prediction.py', 'Machine Learning Prediction'),
    ]
    
    results = {}
    
    for script, description in analyses:
        if os.path.exists(script):
            success = run_analysis(script, description)
            results[description] = success
        else:
            print(f"\n✗ Script not found: {script}")
            results[description] = False
    
    # Print summary
    print("\n" + "="*80)
    print("ANALYSIS SUMMARY")
    print("="*80)
    
    for description, success in results.items():
        status = "✓ SUCCESS" if success else "✗ FAILED"
        print(f"{status}: {description}")
    
    total = len(results)
    successful = sum(results.values())
    
    print(f"\nTotal: {successful}/{total} analyses completed successfully")
    print("\n" + "="*80)
    print("ALL ANALYSES COMPLETE!")
    print("="*80)
    
    print("\nGenerated outputs:")
    print("  • data/spacex_launch_data.csv - Launch data")
    print("  • images/*.png - Visualization charts")
    print("  • maps/*.html - Interactive Folium maps")
    print("  • dashboard/spacex_dashboard.html - Interactive dashboard")
    print("  • reports/*.txt - Analysis reports")

if __name__ == "__main__":
    main()

