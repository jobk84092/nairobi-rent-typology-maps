# Nairobi Wards Rent Analysis

## 📚 Overview  
This project analyzes average and median rental prices across all 85 wards in Nairobi using publicly available real estate data, demographic sources, and official administrative boundaries.

> ⚠️ **Disclaimer**: No government rent statistics exist at the ward level. All figures are derived from market reports (e.g., Knight Frank, Cytonn) and public datasets (KNBS, ArcGIS), with clear geographic mapping.

## 📂 Data Sources  
1. Realtors.co.ke – Average Apartment Prices by Area (2026)  
   https://realtors.co.ke/average-apartment-prices-in-nairobi-by-area/

2. Knight Frank Kenya – Annual Property Market Reports (2019–2025)  
   https://www.knightfrank.com/knowledge-center/research-and-insights  

3. Cytonn Real Estate – Kenya Residential Property Report  
   https://cytonn.co.ke/property-market-overview/

4. KNBS 2019 Census (OpenAFRICA) – Household Rent Data by Sub-County  
   https://open.africa/tr/dataset/2019-kenya-population-and-housing-census/resource/c19bf300-6d83-41f2-a3c0-0896a10f0d30

5. Nairobi Postal Codes – Wards & Sub-Counties (2026)  
   https://nairobipostalcode.org/nairobi-county-sub-counties-wards-locations/

## 📊 Methodology  
- Data was aggregated by ward using a geographic mapping of suburbs to wards.
- Each suburb’s rent range was assigned to relevant wards based on location and market data.
- Final average/median values were computed per ward, with outlier handling via median filtering.

## 🔍 Key Findings  
- Westlands and Kilimani have the highest rental costs.  
- Embakasi and Ruaka are significantly more affordable — but face affordability challenges due to low-income populations.  
- Price differences between regions exceed 2x, highlighting urban inequality.

## 📂 Project Structure  
