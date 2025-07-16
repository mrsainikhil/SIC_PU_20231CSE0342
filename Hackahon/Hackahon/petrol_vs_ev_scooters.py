import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Enhanced styling for plots
plt.style.use('default')
sns.set_palette("husl")
plt.rcParams['figure.figsize'] = [14, 8]
plt.rcParams['font.size'] = 11
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['xtick.labelsize'] = 10
plt.rcParams['ytick.labelsize'] = 10

def analyze_petrol_vs_electric_enhanced():
    
    # Get current folder path
    current_dir = os.path.dirname(os.path.abspath(__file__)) if '__file__' in globals() else os.getcwd()
    
    # Verifying files
    required_files = [
        'scooter_sales_data.xlsx',
        'India_Electric_2Wheeler_Sales.xlsx',
        'EV_Battery_Analysis.xlsx',
        'Top_25_E2W_Manufacturers_FY2025.xlsx'
    ]
    
    missing_files = [f for f in required_files if not os.path.exists(os.path.join(current_dir, f))]
    if missing_files:
        print("Missing files:", missing_files)
        return
    
    print("+"*80)
    print("COMPREHENSIVE ELECTRIC VS PETROL SCOOTER ANALYSIS")
    print("+"*80)
    print("Starting enhanced analysis...\n")
    
    # Helper function to read Excel files 
    def read_excel_safe(filename, sheet_name=None):
        try:
            df = pd.read_excel(os.path.join(current_dir, filename), sheet_name=sheet_name)
            return df.dropna(how='all')
        except Exception as e:
            print(f"Error reading {filename}: {str(e)}")
            return None
    
    # Helper function for consistent formatting
    def format_number(num):
        if num >= 1e6:
            return f"{num/1e6:.2f}M"
        elif num >= 1e3:
            return f"{num/1e3:.1f}K"
        else:
            return f"{num:.0f}"
    
    try:
        # Load all data
        petrol_df = read_excel_safe('scooter_sales_data.xlsx', 'Sales Data')
        electric_sales = read_excel_safe('India_Electric_2Wheeler_Sales.xlsx', 'Monthly Sales')
        battery_df = read_excel_safe('EV_Battery_Analysis.xlsx', 'Battery Data')
        electric_mfg = read_excel_safe('Top_25_E2W_Manufacturers_FY2025.xlsx', 'Top 25 Manufacturers')
        
        if any(df is None for df in [petrol_df, electric_sales, battery_df, electric_mfg]):
            raise ValueError("Could not load all required data files")
                
        # 1. MARKET OVERVIEW & TRENDS
        
        print("\n" + "+"*60)
        print("1. MARKET OVERVIEW & TRENDS")
        print("+"*60)
        
        # Get sales data
        total_petrol = petrol_df.loc[petrol_df['Manufacturer'] == 'Total 2W sales', 'FY2025'].values[0]
        total_electric = electric_sales.iloc[-2]['FY2025']
        
        # Calculate market shares
        total_sales = total_petrol + total_electric
        petrol_share = (total_petrol/total_sales)*100
        electric_share = (total_electric/total_sales)*100
        
        # Growth rate
        petrol_growth = float(str(petrol_df.loc[petrol_df['Manufacturer'] == 'Total 2W sales', 'YoY % change'].values[0]).strip('%'))
        electric_growth = float(str(electric_sales.iloc[-2]['% Change']).strip('%')) if pd.notna(electric_sales.iloc[-2]['% Change']) else 0
        
        # overview of market
        market_overview = pd.DataFrame({
            'Metric': ['Total Sales (Units)', 'Market Share (%)', 'YoY Growth (%)', 'CAGR Projection (%)'],
            'Petrol Scooters': [format_number(total_petrol), f"{petrol_share:.1f}%", f"{petrol_growth:.1f}%", "5-8%"],
            'Electric Scooters': [format_number(total_electric), f"{electric_share:.1f}%", f"{electric_growth:.1f}%", "25-35%"]
        })
        
        print("\nMarket Overview:")
        print(market_overview.to_string(index=False))
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10))
        
        # pie chart of market share
        ax1.pie([petrol_share, electric_share], labels=['Petrol', 'Electric'], 
                autopct='%1.1f%%', startangle=90, explode=(0, 0.1),
                colors=['#FF6B6B', '#4ECDC4'])
        ax1.set_title('Market Share Distribution (FY2025)', fontweight='bold',fontsize=10)
        
        # comparision of sales
        sales_data = pd.DataFrame({
            'Type': ['Petrol', 'Electric'],
            'Sales (Millions)': [total_petrol/1e6, total_electric/1e6]
        })
        bars = ax2.bar(sales_data['Type'], sales_data['Sales (Millions)'], 
                      color=['#FF6B6B', '#4ECDC4'])
        ax2.set_title('Total Sales Volume (FY2025)', fontweight='bold',fontsize=10)
        ax2.set_ylabel('Sales (Millions)')
        for bar in bars:
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.2f}M', ha='center', va='bottom')
        
        # comparision of growth
        growth_data = pd.DataFrame({
            'Type': ['Petrol', 'Electric'],
            'Growth (%)': [petrol_growth, electric_growth]
        })
        bars = ax3.bar(growth_data['Type'], growth_data['Growth (%)'], 
                      color=['#FF6B6B', '#4ECDC4'])
        ax3.set_title('Year-over-Year Growth (FY2025)', fontweight='bold',fontsize=10)
        ax3.set_ylabel('Growth Rate (%)')
        for bar in bars:
            height = bar.get_height()
            ax3.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.1f}%', ha='center', va='bottom')
        
        # future projections of market
        years = np.array([2025, 2026, 2027, 2028, 2030])
        petrol_projection = total_petrol * (1.065 ** (years - 2025))  # 6.5% CAGR
        electric_projection = total_electric * (1.30 ** (years - 2025))  # 30% CAGR
        
        ax4.plot(years, petrol_projection/1e6, marker='o', label='Petrol', linewidth=2, color='#FF6B6B')
        ax4.plot(years, electric_projection/1e6, marker='s', label='Electric', linewidth=2, color='#4ECDC4')
        ax4.set_title('Market Projection (2025-2030)', fontweight='bold',fontsize=10)
        ax4.set_xlabel('Year')
        ax4.set_ylabel('Sales (Millions)')
        ax4.legend()
        ax4.grid(True, alpha=0.3)
        
        plt.suptitle('Electric vs Petrol Scooters: Market Analysis', fontsize=12, fontweight='bold')
        plt.tight_layout()
        plt.show()
        
        # 2.cost of ownership

        print("\n" + "+"*60)
        print("2. TOTAL COST OF OWNERSHIP ANALYSIS")
        print("+"*60)
        
        # cost calculations
        avg_battery_cost = battery_df['Replacement Cost Avg (₹)'].mean()
        avg_battery_life = battery_df['Lifespan Years Avg'].mean()
        
        # breakdown of cost
        years = 10  # 10-year analysis
        annual_km = 12000
        
        # petrol costs
        petrol_price = 105  # Rs/liter
        avg_mileage = 45  # Km/liter
        annual_fuel_cost = (annual_km / avg_mileage) * petrol_price
        
        # electric costs
        electricity_rate = 6  # Rs/kWh
        ev_efficiency = 0.8  # KWh/100Km
        annual_electricity_cost = (annual_km / 100) * ev_efficiency * electricity_rate
        
        # maintenance cost
        petrol_maintenance = [3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000, 11000, 12000]
        electric_maintenance = [1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000, 5500, 6000]
        
        # insurance cost
        insurance_petrol = 4000  # Annual
        insurance_electric = 3500  # Annual
        
        # yearly cost
        yearly_costs = pd.DataFrame({
            'Year': range(1, years + 1),
            'Petrol_Fuel': [annual_fuel_cost] * years,
            'Electric_Electricity': [annual_electricity_cost] * years,
            'Petrol_Maintenance': petrol_maintenance,
            'Electric_Maintenance': electric_maintenance,
            'Petrol_Insurance': [insurance_petrol] * years,
            'Electric_Insurance': [insurance_electric] * years
        })
        
        # battery replacement costs
        battery_replacements = np.zeros(years)
        for year in range(1, years + 1):
            if year % int(avg_battery_life) == 0:
                battery_replacements[year - 1] = avg_battery_cost
        
        yearly_costs['Electric_Battery'] = battery_replacements
        
        # overall cost
        petrol_total = yearly_costs[['Petrol_Fuel', 'Petrol_Maintenance', 'Petrol_Insurance']].sum(axis=1).cumsum()
        electric_total = yearly_costs[['Electric_Electricity', 'Electric_Maintenance', 'Electric_Insurance', 'Electric_Battery']].sum(axis=1).cumsum()
        
        # analysis of cost
        cost_breakdown = pd.DataFrame({
            'Cost Component': ['Fuel/Electricity', 'Maintenance', 'Insurance', 'Battery Replacement', 'Total 10-Year Cost'],
            'Petrol Scooter (₹)': [
                annual_fuel_cost * years,
                sum(petrol_maintenance),
                insurance_petrol * years,
                0,
                petrol_total.iloc[-1]
            ],
            'Electric Scooter (₹)': [
                annual_electricity_cost * years,
                sum(electric_maintenance),
                insurance_electric * years,
                avg_battery_cost * (years / avg_battery_life),
                electric_total.iloc[-1]
            ]
        })
        
        cost_breakdown['Savings with Electric (₹)'] = cost_breakdown['Petrol Scooter (₹)'] - cost_breakdown['Electric Scooter (₹)']
        
        print("\n10-Year Total Cost of Ownership:")
        print(cost_breakdown.to_string(index=False))
        
        # visualize cost analysis
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
        
        # cost over time
        ax1.plot(yearly_costs['Year'], petrol_total, marker='o', label='Petrol', linewidth=2, color='#FF6B6B')
        ax1.plot(yearly_costs['Year'], electric_total, marker='s', label='Electric', linewidth=2, color='#4ECDC4')
        ax1.fill_between(yearly_costs['Year'], petrol_total, electric_total, 
                        where=(petrol_total >= electric_total), alpha=0.3, color='green', label='Savings')
        ax1.set_title('Cumulative Cost Over Time', fontweight='bold',fontsize=10)
        ax1.set_xlabel('Year')
        ax1.set_ylabel('Cumulative Cost (₹)')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # cost breakdown comparison
        categories = ['Fuel/Electricity', 'Maintenance', 'Insurance', 'Battery']
        petrol_costs = [annual_fuel_cost * years, sum(petrol_maintenance), insurance_petrol * years, 0]
        electric_costs = [annual_electricity_cost * years, sum(electric_maintenance), 
                         insurance_electric * years, avg_battery_cost * (years / avg_battery_life)]
        
        x = np.arange(len(categories))
        width = 0.35
        
        bars1 = ax2.bar(x - width/2, petrol_costs, width, label='Petrol', color='#FF6B6B')
        bars2 = ax2.bar(x + width/2, electric_costs, width, label='Electric', color='#4ECDC4')
        
        ax2.set_title('Cost Breakdown Comparison (10 Years)', fontweight='bold',fontsize=10)
        ax2.set_ylabel('Cost (₹)')
        ax2.set_xticks(x)
        ax2.set_xticklabels(categories)
        ax2.legend()
        
        # add value labels on bars
        for bars in [bars1, bars2]:
            for bar in bars:
                height = bar.get_height()
                ax2.text(bar.get_x() + bar.get_width()/2., height,
                        f'₹{height:,.0f}', ha='center', va='bottom', fontsize=9)
        
        plt.tight_layout()
        plt.show()
               
        # 3. ENVIRONMENTAL IMPACT ANALYSIS
        
        print("\n" + "+"*60)
        print("3. ENVIRONMENTAL IMPACT ANALYSIS")
        print("+"*60)
        
        # carbon footprint calculation
        petrol_co2_per_liter = 2.31  # kg CO2 per liter
        electricity_co2_per_kwh = 0.82  # kg CO2 per kWh (India grid average)
        
        # annual emissions
        annual_petrol_liters = annual_km / avg_mileage
        annual_petrol_co2 = annual_petrol_liters * petrol_co2_per_liter
        
        annual_electric_kwh = (annual_km / 100) * ev_efficiency
        annual_electric_co2 = annual_electric_kwh * electricity_co2_per_kwh
        
        # 10-year environmental impact
        lifetime_petrol_co2 = annual_petrol_co2 * years
        lifetime_electric_co2 = annual_electric_co2 * years
        
        # manufacturing footprint (estimated)
        manufacturing_petrol_co2 = 2000  # kg CO2
        manufacturing_electric_co2 = 3500  # kg CO2 (higher due to battery)
        
        # total lifecycle emissions
        total_petrol_co2 = lifetime_petrol_co2 + manufacturing_petrol_co2
        total_electric_co2 = lifetime_electric_co2 + manufacturing_electric_co2
        
        env_impact = pd.DataFrame({
            'Impact Category': ['Annual CO2 Emissions (kg)', 'Lifetime CO2 Emissions (kg)', 
                              'Manufacturing CO2 (kg)', 'Total Lifecycle CO2 (kg)',
                              'Annual Fuel Consumption', 'Noise Pollution (dB)',
                              'Local Air Pollution'],
            'Petrol Scooter': [f"{annual_petrol_co2:.1f}", f"{lifetime_petrol_co2:.1f}",
                             f"{manufacturing_petrol_co2:.1f}", f"{total_petrol_co2:.1f}",
                             f"{annual_petrol_liters:.1f} liters", "75-80", "High"],
            'Electric Scooter': [f"{annual_electric_co2:.1f}", f"{lifetime_electric_co2:.1f}",
                               f"{manufacturing_electric_co2:.1f}", f"{total_electric_co2:.1f}",
                               f"{annual_electric_kwh:.1f} kWh", "45-50", "Zero"]
        })
        
        print("\nEnvironmental Impact Comparison:")
        print(env_impact.to_string(index=False))
        
        co2_savings = total_petrol_co2 - total_electric_co2
        print(f"\nCO2 Savings with Electric: {co2_savings:.1f} kg over 10 years")
        print(f"Equivalent to planting {co2_savings/22:.0f} trees")
        
        # visualize environmental impact
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10))
        
        # annual emissions comparison
        categories = ['Annual CO2 (kg)', 'Lifetime CO2 (kg)', 'Manufacturing CO2 (kg)']
        petrol_emissions = [annual_petrol_co2, lifetime_petrol_co2, manufacturing_petrol_co2]
        electric_emissions = [annual_electric_co2, lifetime_electric_co2, manufacturing_electric_co2]
        
        x = np.arange(len(categories))
        width = 0.35
        
        bars1 = ax1.bar(x - width/2, petrol_emissions, width, label='Petrol', color='#FF6B6B')
        bars2 = ax1.bar(x + width/2, electric_emissions, width, label='Electric', color='#4ECDC4')
        
        ax1.set_title('CO2 Emissions Comparison', fontweight='bold',fontsize=10)
        ax1.set_ylabel('CO2 Emissions (kg)')
        ax1.set_xticks(x)
        ax1.set_xticklabels(categories)
        ax1.legend()
        
        # cumulative emissions over time
        years_range = np.arange(1, years + 1)
        cumulative_petrol = annual_petrol_co2 * years_range + manufacturing_petrol_co2
        cumulative_electric = annual_electric_co2 * years_range + manufacturing_electric_co2
        
        ax2.plot(years_range, cumulative_petrol, marker='o', label='Petrol', linewidth=2, color='#FF6B6B')
        ax2.plot(years_range, cumulative_electric, marker='s', label='Electric', linewidth=2, color='#4ECDC4')
        ax2.fill_between(years_range, cumulative_petrol, cumulative_electric, 
                        where=(cumulative_petrol >= cumulative_electric), alpha=0.3, color='green')
        ax2.set_title('Cumulative CO2 Emissions Over Time', fontweight='bold',fontsize=10)
        ax2.set_xlabel('Year')
        ax2.set_ylabel('Cumulative CO2 (kg)')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # energy consumption comparison
        energy_types = ['Petrol Consumption\n(Liters/Year)', 'Electricity Consumption\n(kWh/Year)']
        energy_values = [annual_petrol_liters, annual_electric_kwh]
        colors = ['#FF6B6B', '#4ECDC4']
        
        bars = ax3.bar(energy_types, energy_values, color=colors)
        ax3.set_title('Annual Energy Consumption', fontweight='bold',fontsize=10)
        ax3.set_ylabel('Energy Units')
        for bar in bars:
            height = bar.get_height()
            ax3.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.1f}', ha='center', va='bottom')
        
        # Noise pollution

        noise_levels = ['Petrol Scooter', 'Electric Scooter']
        noise_values = [77.5, 47.5]  # Average noise levels in dB
        
        bars = ax4.bar(noise_levels, noise_values, color=['#FF6B6B', '#4ECDC4'])
        ax4.set_title('Noise Pollution Levels', fontweight='bold',fontsize=10)
        ax4.set_ylabel('Noise Level (dB)')
        ax4.axhline(y=55, color='red', linestyle='--', alpha=0.7, label='WHO Recommended Limit')
        ax4.legend()
        for bar in bars:
            height = bar.get_height()
            ax4.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.1f} dB', ha='center', va='bottom')
        
        plt.suptitle('Environmental Impact Analysis', fontsize=12, fontweight='bold')
        plt.tight_layout()
        plt.show()
        
        
        # 4. PERFORMANCE & TECHNOLOGY COMPARISON

        print("\n" + "+"*60)
        print("4. PERFORMANCE & TECHNOLOGY COMPARISON")
        print("+"*60)
        
        # performance
        performance_metrics = pd.DataFrame({
            'Metric': ['Top Speed (km/h)', 'Acceleration (0-40 km/h)', 'Range (km)', 
                      'Refuel/Recharge Time', 'Power (kW)', 'Torque (Nm)',
                      'Weight (kg)', 'Efficiency', 'Cold Start Performance'],
            'Petrol Scooter': ['80-90', '8-10 sec', '150-200', '2-3 min', '6-8', '8-10',
                             '100-120', '40-50 km/L', 'Good'],
            'Electric Scooter': ['60-80', '6-8 sec', '80-120', '3-6 hours', '2-4', '15-25',
                               '80-100', '80-100 km/kWh', 'Excellent']
        })
        
        print("\nPerformance Comparison:")
        print(performance_metrics.to_string(index=False))
        
        # features
        tech_features = pd.DataFrame({
            'Feature': ['Instant Torque', 'Smart Connectivity', 'GPS Tracking', 'Mobile App',
                       'Regenerative Braking', 'Multiple Ride Modes', 'Anti-theft System',
                       'Digital Dashboard', 'OTA Updates', 'Maintenance Alerts'],
            'Petrol Scooter': ['No', 'Limited', 'Optional', 'Basic', 'No', 'No', 'Basic',
                             'Analog/Basic', 'No', 'Manual'],
            'Electric Scooter': ['Yes', 'Advanced', 'Standard', 'Comprehensive', 'Yes', 'Yes', 'Advanced',
                               'Fully Digital', 'Yes', 'Automatic']
        })
        
        print("\nTechnology Features Comparison:")
        print(tech_features.to_string(index=False))
        
        # Visualize performance comparison
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10))
        
        # Performance radar chart data
        categories = ['Top Speed', 'Acceleration', 'Range', 'Efficiency', 'Torque']
        petrol_scores = [85, 70, 90, 60, 60]  # Normalized scores out of 100
        electric_scores = [70, 85, 70, 90, 90]
        
        # Convert to radar chart
        angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
        angles += angles[:1]  # Complete the circle
        
        petrol_scores += petrol_scores[:1]
        electric_scores += electric_scores[:1]
        
        ax1 = plt.subplot(2, 2, 1, projection='polar')
        ax1.plot(angles, petrol_scores, 'o-', linewidth=2, label='Petrol', color='#FF6B6B')
        ax1.fill(angles, petrol_scores, alpha=0.25, color='#FF6B6B')
        ax1.plot(angles, electric_scores, 's-', linewidth=2, label='Electric', color='#4ECDC4')
        ax1.fill(angles, electric_scores, alpha=0.25, color='#4ECDC4')
        ax1.set_xticks(angles[:-1])
        ax1.set_xticklabels(categories)
        ax1.set_ylim(0, 100)
        ax1.set_title('Performance Comparison', fontweight='bold',fontsize=10, pad=20)
        ax1.legend()
        
        # Technology adoption score
        ax2 = plt.subplot(2, 2, 2)
        tech_categories = ['Connectivity', 'Safety', 'Convenience', 'Sustainability', 'Innovation']
        petrol_tech = [30, 60, 50, 20, 30]
        electric_tech = [85, 80, 90, 95, 90]
        
        x = np.arange(len(tech_categories))
        width = 0.35
        
        bars1 = ax2.bar(x - width/2, petrol_tech, width, label='Petrol', color='#FF6B6B')
        bars2 = ax2.bar(x + width/2, electric_tech, width, label='Electric', color='#4ECDC4')
        
        ax2.set_title('Technology Adoption Score', fontweight='bold',fontsize=10)
        ax2.set_ylabel('Score (0-100)')
        ax2.set_xticks(x)
        ax2.set_xticklabels(tech_categories, rotation=45)
        ax2.legend()
        
        # Efficiency comparison
        ax3 = plt.subplot(2, 2, 3)
        efficiency_data = pd.DataFrame({
            'Vehicle Type': ['Petrol', 'Electric'],
            'Energy Efficiency (km/unit)': [45, 90],  # km/liter vs km/kWh equivalent
            'Cost per km (₹)': [2.33, 0.58]  # Cost per km
        })
        
        ax3_twin = ax3.twinx()
        
        bars1 = ax3.bar(efficiency_data['Vehicle Type'], efficiency_data['Energy Efficiency (km/unit)'], 
                       alpha=0.7, color=['#FF6B6B', '#4ECDC4'], label='Efficiency')
        line1 = ax3_twin.plot(efficiency_data['Vehicle Type'], efficiency_data['Cost per km (₹)'], 
                             'ko-', linewidth=2, markersize=8, label='Cost/km')
        
        ax3.set_title('Efficiency & Cost Comparison', fontweight='bold',fontsize=10)
        ax3.set_ylabel('Energy Efficiency (km/unit)')
        ax3_twin.set_ylabel('Cost per km (₹)')
        
        # Maintenance requirements
        ax4 = plt.subplot(2, 2, 4)
        maintenance_freq = pd.DataFrame({
            'Service Type': ['Oil Change', 'Filter Replacement', 'Spark Plug', 'Battery Check', 
                           'Brake Service', 'Software Update'],
            'Petrol Frequency (months)': [3, 6, 12, 12, 12, 0],
            'Electric Frequency (months)': [0, 0, 0, 6, 18, 3]
        })
        
        service_types = maintenance_freq['Service Type']
        petrol_freq = maintenance_freq['Petrol Frequency (months)']
        electric_freq = maintenance_freq['Electric Frequency (months)']
        
        x = np.arange(len(service_types))
        width = 0.35
        
        bars1 = ax4.bar(x - width/2, petrol_freq, width, label='Petrol', color='#FF6B6B')
        bars2 = ax4.bar(x + width/2, electric_freq, width, label='Electric', color='#4ECDC4')
        
        ax4.set_title('Maintenance Frequency', fontweight='bold',fontsize=10)
        ax4.set_ylabel('Frequency (months)')
        ax4.set_xticks(x)
        ax4.set_xticklabels(service_types, rotation=45)
        ax4.legend()
        
        plt.tight_layout()
        plt.show()
        
        
        # 5. INFRASTRUCTURE & ECOSYSTEM ANALYSIS
        
        print("\n" + "+"*60)
        print("5. INFRASTRUCTURE & ECOSYSTEM ANALYSIS")
        print("+"*60)
        
        # Infrastructure data (estimated for major Indian cities)
        infrastructure = pd.DataFrame({
            'Infrastructure Type': ['Fuel Stations', 'Charging Stations', 'Service Centers',
                                  'Spare Parts Availability', 'Charging Time', 'Accessibility'],
            'Petrol Scooter': ['~70,000', '0', '~15,000', 'Excellent', '2-3 min', 'Universal'],
            'Electric Scooter': ['0', '~5,000', '~2,000', 'Good', '3-6 hours', 'Growing']
        })
        
        print("\nInfrastructure Comparison:")
        print(infrastructure.to_string(index=False))
        
        # Government incentives
        incentives = pd.DataFrame({
            'Incentive Type': ['FAME-II Subsidy', 'State Subsidies', 'Road Tax Exemption',
                             'Registration Fee Waiver', 'Insurance Discount', 'Loan Interest Rate'],
            'Petrol Scooter': ['₹0', '₹0', 'Standard', 'Standard', 'Standard', '12-15%'],
            'Electric Scooter': ['₹10,000-15,000', '₹5,000-25,000', 'Waived', 'Waived', '10-15% off', '8-12%']
        })
        
        print("\nGovernment Incentives:")
        print(incentives.to_string(index=False))
        
        # Visualize infrastructure analysis
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10))
        
        # Infrastructure availability
        infra_categories = ['Fuel/Charge Stations', 'Service Centers']
        petrol_infra = [70000, 15000]
        electric_infra = [5000, 2000]
        
        x = np.arange(len(infra_categories))
        width = 0.35
        
        bars1 = ax1.bar(x - width/2, petrol_infra, width, label='Petrol', color='#FF6B6B')
        bars2 = ax1.bar(x + width/2, electric_infra, width, label='Electric', color='#4ECDC4')
        
        ax1.set_title('Infrastructure Availability in India', fontweight='bold',fontsize=10)
        ax1.set_ylabel('Number of Stations/Centers')
        ax1.set_xticks(x)
        ax1.set_xticklabels(infra_categories)
        ax1.legend()
        ax1.set_yscale('log')  # Log scale due to large difference
        
        # Charging vs Refueling time
        refuel_data = pd.DataFrame({
            'Type': ['Petrol Refuel', 'Electric Charge (Fast)', 'Electric Charge (Normal)'],
            'Time (minutes)': [3, 45, 240],
            'Range Added (km)': [150, 60, 100]
        })
        
        ax2_twin = ax2.twinx()
        bars = ax2.bar(refuel_data['Type'], refuel_data['Time (minutes)'], 
                      color=['#FF6B6B', '#4ECDC4', '#95E1D3'], alpha=0.7)
        line = ax2_twin.plot(refuel_data['Type'], refuel_data['Range Added (km)'], 
                           'ko-', linewidth=2, markersize=8)
        
        ax2.set_title('Refuel/Recharge Time vs Range', fontweight='bold',fontsize=10)
        ax2.set_ylabel('Time (minutes)')
        ax2_twin.set_ylabel('Range Added (km)')
        ax2.set_xticklabels(refuel_data['Type'], rotation=45)
        
        # Government incentive value
        incentive_values = pd.DataFrame({
            'Incentive': ['FAME-II', 'State Subsidy', 'Tax Benefits'],
            'Petrol (₹)': [0, 0, 0],
            'Electric (₹)': [12500, 15000, 8000]
        })
        
        x = np.arange(len(incentive_values))
        width = 0.35
        
        bars1 = ax3.bar(x - width/2, incentive_values['Petrol (₹)'], width, 
                       label='Petrol', color='#FF6B6B')
        bars2 = ax3.bar(x + width/2, incentive_values['Electric (₹)'], width, 
                       label='Electric', color='#4ECDC4')
        
        ax3.set_title('Government Incentives Value', fontweight='bold',fontsize=10)
        ax3.set_ylabel('Incentive Amount (₹)')
        ax3.set_xticks(x)
        ax3.set_xticklabels(incentive_values['Incentive'])
        ax3.legend()
        
        # Infrastructure growth projection
        years_infra = np.arange(2025, 2031)
        petrol_stations = np.array([70000, 72000, 74000, 76000, 78000, 80000])
        electric_stations = np.array([5000, 8000, 15000, 25000, 40000, 60000])
        
        ax4.plot(years_infra, petrol_stations, marker='o', label='Petrol Stations', 
                linewidth=2, color='#FF6B6B')
        ax4.plot(years_infra, electric_stations, marker='s', label='Charging Stations', 
                linewidth=2, color='#4ECDC4')
        
        ax4.set_title('Infrastructure Growth Projection', fontweight='bold',fontsize=10)
        ax4.set_xlabel('Year')
        ax4.set_ylabel('Number of Stations')
        ax4.legend()
        ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()
        
        
        # 6. CONSUMER BEHAVIOR & ADOPTION ANALYSIS
        
        print("\n" + "+"*60)
        print("6. CONSUMER BEHAVIOR & ADOPTION ANALYSIS")
        print("+"*60)
        
        # Consumer preference factors
        preference_factors = pd.DataFrame({
            'Factor': ['Purchase Price', 'Running Cost', 'Maintenance', 'Environment',
                      'Performance', 'Convenience', 'Brand Trust', 'Technology'],
            'Importance (1-10)': [9, 8, 7, 6, 8, 9, 8, 7],
            'Petrol Score': [8, 6, 5, 3, 7, 9, 9, 5],
            'Electric Score': [6, 9, 8, 10, 6, 6, 6, 9]
        })
        
        print("\nConsumer Preference Analysis:")
        print(preference_factors.to_string(index=False))
        
        # Calculate weighted scores
        preference_factors['Petrol Weighted'] = preference_factors['Importance (1-10)'] * preference_factors['Petrol Score']
        preference_factors['Electric Weighted'] = preference_factors['Importance (1-10)'] * preference_factors['Electric Score']
        
        total_petrol_score = preference_factors['Petrol Weighted'].sum()
        total_electric_score = preference_factors['Electric Weighted'].sum()
        
        print(f"\nOverall Consumer Preference Scores:")
        print(f"Petrol Scooters: {total_petrol_score}/800")
        print(f"Electric Scooters: {total_electric_score}/800")
        
        # Adoption barriers
        barriers = pd.DataFrame({
            'Barrier': ['High Initial Cost', 'Limited Range', 'Charging Infrastructure',
                       'Charging Time', 'Battery Replacement', 'Brand Awareness',
                       'Service Network', 'Resale Value Uncertainty'],
            'Severity (1-10)': [8, 7, 9, 8, 7, 6, 7, 8],
            'Trend': ['Improving', 'Improving', 'Improving', 'Improving', 
                     'Stable', 'Improving', 'Improving', 'Stable']
        })
        
        print("\nAdoption Barriers for Electric Scooters:")
        print(barriers.to_string(index=False))
        
        # Visualize consumer analysis
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10))
        
        # Consumer preference radar chart
        categories = preference_factors['Factor'].tolist()
        petrol_scores = preference_factors['Petrol Score'].tolist()
        electric_scores = preference_factors['Electric Score'].tolist()
        
        angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
        angles += angles[:1]
        
        petrol_scores += petrol_scores[:1]
        electric_scores += electric_scores[:1]
        
        ax1 = plt.subplot(2, 2, 1, projection='polar')
        ax1.plot(angles, petrol_scores, 'o-', linewidth=2, label='Petrol', color='#FF6B6B')
        ax1.fill(angles, petrol_scores, alpha=0.25, color='#FF6B6B')
        ax1.plot(angles, electric_scores, 's-', linewidth=2, label='Electric', color='#4ECDC4')
        ax1.fill(angles, electric_scores, alpha=0.25, color='#4ECDC4')
        ax1.set_xticks(angles[:-1])
        ax1.set_xticklabels(categories, fontsize=9)
        ax1.set_ylim(0, 10)
        ax1.set_title('Consumer Preference Factors', fontweight='bold',fontsize=10, pad=20)
        ax1.legend()
        
        # Adoption barriers
        ax2 = plt.subplot(2, 2, 2)
        barrier_names = barriers['Barrier']
        severity = barriers['Severity (1-10)']
        colors = ['#FF6B6B' if trend == 'Stable' else '#4ECDC4' for trend in barriers['Trend']]
        
        bars = ax2.barh(barrier_names, severity, color=colors)
        ax2.set_title('Electric Scooter Adoption Barriers', fontweight='bold',fontsize=10)
        ax2.set_xlabel('Severity (1-10)')
        
        # Market segment analysis
        ax3 = plt.subplot(2, 2, 3)
        segments = ['Budget\n(<₹60k)', 'Mid-range\n(₹60k-₹1L)', 'Premium\n(>₹1L)']
        petrol_segments = [70, 25, 5]
        electric_segments = [40, 45, 15]
        
        x = np.arange(len(segments))
        width = 0.35
        
        bars1 = ax3.bar(x - width/2, petrol_segments, width, label='Petrol', color='#FF6B6B')
        bars2 = ax3.bar(x + width/2, electric_segments, width, label='Electric', color='#4ECDC4')
        
        ax3.set_title('Market Segment Distribution (%)', fontweight='bold',fontsize=10)
        ax3.set_ylabel('Market Share (%)')
        ax3.set_xticks(x)
        ax3.set_xticklabels(segments)
        ax3.legend()
        
        # Adoption timeline prediction
        ax4 = plt.subplot(2, 2, 4)
        years_adoption = np.arange(2025, 2031)
        petrol_adoption = np.array([85, 80, 75, 65, 55, 45])
        electric_adoption = np.array([15, 20, 25, 35, 45, 55])
        
        ax4.plot(years_adoption, petrol_adoption, marker='o', label='Petrol Market Share', 
                linewidth=2, color='#FF6B6B')
        ax4.plot(years_adoption, electric_adoption, marker='s', label='Electric Market Share', 
                linewidth=2, color='#4ECDC4')
        ax4.axhline(y=50, color='gray', linestyle='--', alpha=0.7, label='50% Market Share')
        
        ax4.set_title('Market Share Evolution Prediction', fontweight='bold',fontsize=10)
        ax4.set_xlabel('Year')
        ax4.set_ylabel('Market Share (%)')
        ax4.legend()
        ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()
        
        
        # 7. MANUFACTURER ECOSYSTEM ANALYSIS
        
        print("\n" + "+"*60)
        print("7. MANUFACTURER ECOSYSTEM ANALYSIS")
        print("+"*60)
        
        # Process manufacturer data
        petrol_mfg = petrol_df[~petrol_df['Manufacturer'].str.contains('Total', na=False)]
        petrol_mfg = petrol_mfg.sort_values('FY2025', ascending=False).head(10)
        
        # Process electric manufacturer data
        if len(electric_mfg) > 25:
            electric_mfg = electric_mfg.iloc[1:26]
        
        manufacturer_col = None
        for col in ['Manufacturer', 'Company', 'Brand', 'Name', '1']:
            if col in electric_mfg.columns:
                manufacturer_col = col
                break
        
        if manufacturer_col is None:
            manufacturer_col = electric_mfg.columns[0]
        
        # Calculate total sales if not present
        if 'Total' not in electric_mfg.columns:
            numeric_cols = electric_mfg.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) > 0:
                electric_mfg['Total'] = electric_mfg[numeric_cols].sum(axis=1)
            else:
                for col in electric_mfg.columns:
                    if col != manufacturer_col:
                        electric_mfg[col] = pd.to_numeric(electric_mfg[col], errors='coerce')
                numeric_cols = electric_mfg.select_dtypes(include=[np.number]).columns
                electric_mfg['Total'] = electric_mfg[numeric_cols].sum(axis=1)
        
        electric_mfg['Total'] = pd.to_numeric(electric_mfg['Total'], errors='coerce')
        electric_mfg = electric_mfg.dropna(subset=['Total']).sort_values('Total', ascending=False).head(10)
        
        # Market concentration analysis
        petrol_top3 = petrol_mfg.head(3)['FY2025'].sum()
        petrol_hhi = sum((petrol_mfg['FY2025'] / petrol_mfg['FY2025'].sum()) ** 2)
        
        electric_top3 = electric_mfg.head(3)['Total'].sum()
        electric_hhi = sum((electric_mfg['Total'] / electric_mfg['Total'].sum()) ** 2)
        
        market_concentration = pd.DataFrame({
            'Metric': ['Top 3 Market Share (%)', 'HHI (Concentration Index)', 'Market Structure'],
            'Petrol Market': [f"{(petrol_top3/petrol_mfg['FY2025'].sum())*100:.1f}%", 
                            f"{petrol_hhi:.3f}", 'Moderately Concentrated'],
            'Electric Market': [f"{(electric_top3/electric_mfg['Total'].sum())*100:.1f}%", 
                              f"{electric_hhi:.3f}", 'Highly Concentrated']
        })
        
        print("\nMarket Concentration Analysis:")
        print(market_concentration.to_string(index=False))
        
        # Manufacturer performance
        print(f"\nTop 5 Petrol Scooter Manufacturers:")
        petrol_top5 = petrol_mfg.head(5)[['Manufacturer', 'FY2025', 'YoY % change']].copy()
        petrol_top5['Market Share (%)'] = (petrol_top5['FY2025'] / petrol_mfg['FY2025'].sum()) * 100
        print(petrol_top5.to_string(index=False))
        
        print(f"\nTop 5 Electric Scooter Manufacturers:")
        electric_top5 = electric_mfg.head(5)[[manufacturer_col, 'Total']].copy()
        electric_top5['Market Share (%)'] = (electric_top5['Total'] / electric_mfg['Total'].sum()) * 100
        electric_top5.columns = ['Manufacturer', 'FY2025', 'Market Share (%)']
        print(electric_top5.to_string(index=False))
        
        # Visualize manufacturer analysis
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10))
        
        # Top manufacturers comparison
        top_petrol = petrol_mfg.head(5)
        top_electric = electric_mfg.head(5)
        
        ax1.barh(top_petrol['Manufacturer'], top_petrol['FY2025'], 
                color='#FF6B6B', alpha=0.7, label='Petrol')
        ax1.set_title('Top 5 Petrol Manufacturers', fontweight='bold',fontsize=10)
        ax1.set_xlabel('Sales (Units)')
        
        ax2.barh(top_electric[manufacturer_col], top_electric['Total'], 
                color='#4ECDC4', alpha=0.7, label='Electric')
        ax2.set_title('Top 5 Electric Manufacturers', fontweight='bold',fontsize=10)
        ax2.set_xlabel('Sales (Units)')
        
        # Market share pie charts
        ax3.pie(petrol_top5['Market Share (%)'], labels=petrol_top5['Manufacturer'], 
               autopct='%1.1f%%', startangle=90)
        ax3.set_title('Petrol Market Share Distribution', fontweight='bold',fontsize=10)
        
        ax4.pie(electric_top5['Market Share (%)'], labels=electric_top5['Manufacturer'], 
               autopct='%1.1f%%', startangle=90)
        ax4.set_title('Electric Market Share Distribution', fontweight='bold',fontsize=10)
        
        plt.tight_layout()
        plt.show()
        
        
        # 8. FUTURE OUTLOOK & PREDICTIONS
        
        print("\n" + "+"*60)
        print("8. FUTURE OUTLOOK & PREDICTIONS")
        print("+"*60)
        
        # Technology roadmap
        tech_roadmap = pd.DataFrame({
            'Timeline': ['2025-2026', '2027-2028', '2029-2030'],
            'Electric Technology': ['Improved battery density, 150km range', 
                                  'Solid-state batteries, 200km range', 
                                  'Wireless charging, 300km range'],
            'Petrol Technology': ['BS-VII norms, minor efficiency gains', 
                                'Hybrid variants introduction', 
                                'Phase-out regulations'],
            'Infrastructure': ['20k charging stations', '50k charging stations', 
                             '100k charging stations'],
            'Market Prediction': ['20% electric share', '40% electric share', 
                                '60% electric share']
        })
        
        print("\nTechnology & Market Roadmap:")
        print(tech_roadmap.to_string(index=False))
        
        # Key predictions
        predictions = pd.DataFrame({
            'Aspect': ['Market Share by 2030', 'Average Price Convergence', 'Range Improvement',
                      'Charging Infrastructure', 'Battery Life', 'Government Support'],
            'Prediction': ['60% Electric, 40% Petrol', '2027-2028', '300km by 2030',
                          '100k+ stations by 2030', '8-10 years by 2030', 'Continued till 2030']
        })
        
        print("\nKey Predictions:")
        print(predictions.to_string(index=False))
        
        # SWOT Analysis
        print("\n" + "+"*40)
        print("SWOT ANALYSIS")
        print("+"*40)
        
        swot_electric = pd.DataFrame({
            'Strengths': ['Lower running costs', 'Zero emissions', 'Instant torque', 'Government support'],
            'Weaknesses': ['High initial cost', 'Limited range', 'Charging time', 'Infrastructure gaps'],
            'Opportunities': ['Growing environmental awareness', 'Improving technology', 'Policy support', 'Corporate adoption'],
            'Threats': ['Battery degradation', 'Competition from petrol', 'Economic slowdown', 'Raw material costs']
        })
        
        print("\nElectric Scooters SWOT:")
        for category in swot_electric.columns:
            print(f"\n{category}:")
            for item in swot_electric[category]:
                print(f"  • {item}")
        
        # Final visualization - Future market evolution
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10))
        
        # Market evolution timeline
        future_years = np.arange(2025, 2031)
        petrol_future = np.array([85, 80, 70, 60, 50, 40])
        electric_future = np.array([15, 20, 30, 40, 50, 60])
        
        ax1.fill_between(future_years, 0, petrol_future, alpha=0.7, color='#FF6B6B', label='Petrol')
        ax1.fill_between(future_years, petrol_future, 100, alpha=0.7, color='#4ECDC4', label='Electric')
        ax1.plot(future_years, petrol_future, 'o-', color='#FF6B6B', linewidth=2)
        ax1.plot(future_years, electric_future, 's-', color='#4ECDC4', linewidth=2)
        
        ax1.set_title('Market Share Evolution (2025-2030)', fontweight='bold',fontsize=10)
        ax1.set_xlabel('Year')
        ax1.set_ylabel('Market Share (%)')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Technology advancement timeline
        tech_metrics = ['Range (km)', 'Charging Time (min)', 'Battery Life (years)', 'Cost Reduction (%)']
        current_values = [100, 240, 5, 0]
        future_values = [300, 60, 10, 40]
        
        x = np.arange(len(tech_metrics))
        width = 0.35
        
        bars1 = ax2.bar(x - width/2, current_values, width, label='2025', color='#FF6B6B')
        bars2 = ax2.bar(x + width/2, future_values, width, label='2030', color='#4ECDC4')
        
        ax2.set_title('Electric Technology Evolution', fontweight='bold',fontsize=10)
        ax2.set_ylabel('Value')
        ax2.set_xticks(x)
        ax2.set_xticklabels(tech_metrics, rotation=45)
        ax2.legend()
        
        # Investment and policy impact
        policy_impact = pd.DataFrame({
            'Policy': ['FAME-II Extension', 'State Incentives', 'ICE Phase-out', 'Charging Infrastructure'],
            'Impact Score': [8, 7, 9, 8],
            'Timeline': [2025, 2026, 2030, 2028]
        })
        
        colors = plt.cm.viridis(np.linspace(0, 1, len(policy_impact)))
        bars = ax3.bar(policy_impact['Policy'], policy_impact['Impact Score'], color=colors)
        ax3.set_title('Policy Impact on Electric Adoption', fontweight='bold',fontsize=10)
        ax3.set_ylabel('Impact Score (1-10)')
        ax3.set_xticklabels(policy_impact['Policy'], rotation=45)
        
        # Risk-reward matrix
        risk_levels = ['Low Risk\nHigh Reward', 'Medium Risk\nHigh Reward', 'High Risk\nMedium Reward']
        petrol_position = 2  # High risk, medium reward
        electric_position = 1  # Medium risk, high reward
        
        positions = [0, 1, 2]
        petrol_marker = [0, 0, 1]
        electric_marker = [0, 1, 0]
        
        ax4.bar(positions, petrol_marker, alpha=0.7, color='#FF6B6B', label='Petrol Investment')
        ax4.bar(positions, electric_marker, alpha=0.7, color='#4ECDC4', label='Electric Investment')
        
        ax4.set_title('Investment Risk-Reward Matrix', fontweight='bold',fontsize=10)
        ax4.set_ylabel('Investment Attractiveness')
        ax4.set_xticks(positions)
        ax4.set_xticklabels(risk_levels)
        ax4.legend()
        
        plt.tight_layout()
        plt.show()
        
        # 9. EXECUTIVE SUMMARY

        print("\n" + "+"*60)
        print("9. EXECUTIVE SUMMARY")
        print("+"*60)
        
        # Calculate savings using correct variable names
        savings_10_year = petrol_total.iloc[-1] - electric_total.iloc[-1]
        co2_reduction = total_petrol_co2 - total_electric_co2
        
        print(f"""
KEY FINDINGS:

Market Position:
• Electric scooters hold {electric_share:.1f}% market share vs {petrol_share:.1f}% for petrol
• Electric segment growing at {electric_growth:.1f}% vs {petrol_growth:.1f}% for petrol
• Projected to reach 60% market share by 2030

Financial Analysis:
• 10-year ownership cost savings: ₹{savings_10_year:,.0f} with electric
• Electric running cost: ₹{annual_electricity_cost:,.0f}/year vs ₹{annual_fuel_cost:,.0f}/year for petrol
• Break-even point: ~3 years for electric scooters

Environmental Impact:
• CO2 reduction: {co2_reduction:.0f} kg over 10 years
• Equivalent to planting {co2_reduction/22:.0f} trees
• Zero local air pollution with electric

Technology & Performance:
• Electric offers superior torque and acceleration
• Petrol leads in range and refueling convenience
• Electric advancing rapidly in all metrics

Infrastructure:
• Current gap: 70k petrol stations vs 5k charging stations
• Projected 100k+ charging stations by 2030
• Government incentives worth ₹35,000+ for electric

RECOMMENDATIONS:

For Consumers:
• Consider electric for city commuting (<100km daily)
• Petrol remains viable for long-distance travel
• Factor in local charging infrastructure

For Manufacturers:
• Invest heavily in electric R&D and infrastructure
• Focus on battery technology and charging solutions
• Prepare for market transition by 2030

For Policymakers:
• Continue FAME-II and state incentive programs
• Accelerate charging infrastructure development
• Consider ICE phase-out timeline by 2035
        """)
        
        print("\n" + "+"*60)
        print("ANALYSIS COMPLETED SUCCESSFULLY")
        print("+"*60)
        
    except Exception as e:
        print(f"\nError during analysis: {str(e)}")
        import traceback
        traceback.print_exc()

# Run the enhanced analysis
if __name__ == "__main__":
    analyze_petrol_vs_electric_enhanced()