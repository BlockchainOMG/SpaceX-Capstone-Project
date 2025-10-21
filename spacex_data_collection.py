"""
SpaceX Falcon 9 First Stage Landing Prediction
Part 1: Data Collection using SpaceX API

This script collects historical launch data from SpaceX API
and prepares it for analysis.
"""

import requests
import pandas as pd
import json
from datetime import datetime

class SpaceXDataCollector:
    """Class to collect and process SpaceX launch data"""
    
    def __init__(self):
        self.base_url = "https://api.spacexdata.com/v4"
        self.launches_url = f"{self.base_url}/launches/past"
        self.rockets_url = f"{self.base_url}/rockets"
        self.launchpads_url = f"{self.base_url}/launchpads"
        self.payloads_url = f"{self.base_url}/payloads"
        
    def get_launches(self):
        """Fetch all past launches from SpaceX API"""
        try:
            response = requests.get(self.launches_url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching launches: {e}")
            return []
    
    def get_rocket_info(self, rocket_id):
        """Fetch rocket information"""
        try:
            response = requests.get(f"{self.rockets_url}/{rocket_id}")
            return response.json()
        except:
            return {}
    
    def get_launchpad_info(self, launchpad_id):
        """Fetch launchpad information"""
        try:
            response = requests.get(f"{self.launchpads_url}/{launchpad_id}")
            return response.json()
        except:
            return {}
    
    def get_payload_info(self, payload_id):
        """Fetch payload information"""
        try:
            response = requests.get(f"{self.payloads_url}/{payload_id}")
            return response.json()
        except:
            return {}
    
    def extract_launch_features(self, launch):
        """Extract relevant features from launch data"""
        features = {}
        
        # Basic launch information
        features['FlightNumber'] = launch.get('flight_number', None)
        features['Date'] = launch.get('date_utc', None)
        features['LaunchSite'] = launch.get('launchpad', None)
        features['Rocket'] = launch.get('rocket', None)
        features['Success'] = launch.get('success', None)
        features['Name'] = launch.get('name', 'Unknown')
        
        # Core information (first stage)
        cores = launch.get('cores', [])
        if cores and len(cores) > 0:
            core = cores[0]
            features['Core'] = core.get('core', None)
            features['GridFins'] = core.get('gridfins', False)
            features['Reused'] = core.get('reused', False)
            features['Legs'] = core.get('legs', False)
            features['LandingAttempt'] = core.get('landing_attempt', False)
            features['LandingSuccess'] = core.get('landing_success', None)
            features['LandingType'] = core.get('landing_type', None)
            features['LandPad'] = core.get('landpad', None)
        else:
            features['GridFins'] = False
            features['Reused'] = False
            features['Legs'] = False
            features['LandingAttempt'] = False
            features['LandingSuccess'] = None
            features['LandingType'] = None
            
        # Payload information
        payloads = launch.get('payloads', [])
        features['PayloadCount'] = len(payloads)
        
        # Payload mass (sum of all payloads)
        total_payload_mass = 0
        payload_types = []
        for payload_id in payloads:
            payload = self.get_payload_info(payload_id)
            mass = payload.get('mass_kg', 0)
            if mass:
                total_payload_mass += mass
            payload_type = payload.get('type', 'Unknown')
            if payload_type not in payload_types:
                payload_types.append(payload_type)
        
        features['PayloadMass'] = total_payload_mass
        features['PayloadType'] = ', '.join(payload_types) if payload_types else 'Unknown'
        
        # Orbit information
        if payloads:
            payload = self.get_payload_info(payloads[0])
            features['Orbit'] = payload.get('orbit', 'Unknown')
        else:
            features['Orbit'] = 'Unknown'
        
        return features
    
    def create_dataframe(self):
        """Create a pandas DataFrame from SpaceX launch data"""
        print("Fetching launch data from SpaceX API...")
        launches = self.get_launches()
        print(f"Total launches collected: {len(launches)}")
        
        print("Extracting features from launches...")
        launch_features = []
        for i, launch in enumerate(launches):
            if (i + 1) % 50 == 0:
                print(f"Processed {i + 1}/{len(launches)} launches...")
            features = self.extract_launch_features(launch)
            launch_features.append(features)
        
        print("Creating DataFrame...")
        df = pd.DataFrame(launch_features)
        
        # Filter for Falcon 9 rockets
        print("Filtering for Falcon 9 rockets...")
        df_falcon9 = df[df['FlightNumber'].notna()].copy()
        
        # Convert date to datetime
        df_falcon9['Date'] = pd.to_datetime(df_falcon9['Date'])
        
        # Create target variable (Class)
        # 1 if landing was successful, 0 otherwise
        df_falcon9['Class'] = df_falcon9['LandingSuccess'].apply(
            lambda x: 1 if x == True else 0
        )
        
        print(f"\nFalcon 9 launches: {len(df_falcon9)}")
        print(f"Successful landings: {df_falcon9['Class'].sum()}")
        print(f"Failed/No landings: {len(df_falcon9) - df_falcon9['Class'].sum()}")
        
        return df_falcon9
    
    def save_data(self, df, filename='data/spacex_launch_data.csv'):
        """Save DataFrame to CSV"""
        df.to_csv(filename, index=False)
        print(f"\nData saved to {filename}")
        return filename

def main():
    """Main function to run data collection"""
    collector = SpaceXDataCollector()
    df = collector.create_dataframe()
    
    # Display data summary
    print("\n" + "="*50)
    print("DATA SUMMARY")
    print("="*50)
    print(f"\nDataFrame shape: {df.shape}")
    print(f"\nColumns: {list(df.columns)}")
    print(f"\nMissing values:")
    print(df.isnull().sum())
    print(f"\nData types:")
    print(df.dtypes)
    print(f"\nFirst few rows:")
    print(df.head())
    
    # Save data
    collector.save_data(df)
    
    return df

if __name__ == "__main__":
    df = main()

