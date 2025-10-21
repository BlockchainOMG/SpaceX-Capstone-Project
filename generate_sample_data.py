"""
Generate sample SpaceX launch data for demonstration purposes
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_sample_spacex_data(n_samples=100):
    """Generate sample SpaceX launch data"""
    np.random.seed(42)
    
    # Launch sites
    launch_sites = ['CCAFS LC-40', 'CCAFS SLC-40', 'KSC LC-39A', 'VAFB SLC-4E']
    
    # Orbit types
    orbits = ['LEO', 'ISS', 'GTO', 'SSO', 'PO', 'MEO', 'ES-L1']
    
    # Generate dates
    start_date = datetime(2010, 6, 4)
    dates = [start_date + timedelta(days=int(x)) for x in np.sort(np.random.uniform(0, 4000, n_samples))]
    
    data = []
    
    for i, date in enumerate(dates):
        flight_number = i + 1
        
        # Determine features based on flight number (simulate improvement over time)
        progress = i / n_samples
        
        # GridFins, Legs, Reused become more common over time
        grid_fins = np.random.random() < (0.2 + 0.6 * progress)
        legs = np.random.random() < (0.3 + 0.6 * progress)
        reused = np.random.random() < (0.1 + 0.4 * progress)
        
        # Landing attempt more common over time
        landing_attempt = np.random.random() < (0.5 + 0.4 * progress)
        
        # Success rate improves with time and with better equipment
        base_success_rate = 0.3 + 0.5 * progress
        if grid_fins:
            base_success_rate += 0.15
        if legs:
            base_success_rate += 0.15
        if reused:
            base_success_rate -= 0.05  # Slightly harder with reused
        
        landing_success = (np.random.random() < base_success_rate) if landing_attempt else False
        
        # Other features
        launch_site = np.random.choice(launch_sites, p=[0.35, 0.25, 0.25, 0.15])
        orbit = np.random.choice(orbits, p=[0.3, 0.2, 0.15, 0.1, 0.1, 0.1, 0.05])
        payload_mass = np.random.uniform(500, 15000)
        payload_count = np.random.randint(1, 4)
        
        # Landing type
        if landing_attempt:
            landing_type = np.random.choice(['ASDS', 'RTLS', None], p=[0.6, 0.3, 0.1])
        else:
            landing_type = None
        
        data.append({
            'FlightNumber': flight_number,
            'Date': date.strftime('%Y-%m-%d'),
            'LaunchSite': launch_site,
            'Rocket': 'Falcon 9',
            'Success': True,  # Mission success
            'Name': f'Falcon 9 Flight {flight_number}',
            'Core': f'B10{i:02d}',
            'GridFins': grid_fins,
            'Reused': reused,
            'Legs': legs,
            'LandingAttempt': landing_attempt,
            'LandingSuccess': landing_success,
            'LandingType': landing_type,
            'LandPad': 'LZ-1' if landing_type == 'RTLS' else 'OCISLY' if landing_type == 'ASDS' else None,
            'PayloadCount': payload_count,
            'PayloadMass': payload_mass,
            'PayloadType': 'Satellite',
            'Orbit': orbit,
            'Class': 1 if landing_success else 0
        })
    
    df = pd.DataFrame(data)
    return df

def main():
    """Generate and save sample data"""
    print("Generating sample SpaceX launch data...")
    
    # Generate data
    df = generate_sample_spacex_data(n_samples=100)
    
    # Create data directory
    import os
    os.makedirs('data', exist_ok=True)
    
    # Save to CSV
    output_file = 'data/spacex_launch_data.csv'
    df.to_csv(output_file, index=False)
    
    print(f"\n✓ Generated {len(df)} launch records")
    print(f"✓ Saved to {output_file}")
    print(f"\nData summary:")
    print(f"  Total launches: {len(df)}")
    print(f"  Landing attempts: {df['LandingAttempt'].sum()}")
    print(f"  Successful landings: {df['Class'].sum()}")
    print(f"  Success rate: {df['Class'].mean()*100:.2f}%")
    print(f"  Date range: {df['Date'].min()} to {df['Date'].max()}")
    
    print(f"\nFirst few rows:")
    print(df.head())

if __name__ == "__main__":
    main()

