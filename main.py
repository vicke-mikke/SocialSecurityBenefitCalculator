import streamlit as st
import pandas as pd
import numpy as np
import datetime as dt
from calculate_pia import calculate_pia
import plotly.express as px
import plotly.graph_objects as go

def main():    
    # read the csv files
    AWI=pd.read_csv('AWI.csv')
    TSSE_limit=pd.read_csv('Taxed_Social_Security_Earnings_Limit.csv')
    TSSE = pd.read_csv('historical_earnings.csv')

    st.markdown('''# Input Table
You can edit this table. Or copy and paste your table here. * Only numbers   
Your taxed social security earnings history can be found at [ssa.gov](https://www.ssa.gov/myaccount/)               
''')   
    
    edited_df = st.data_editor(TSSE, num_rows="dynamic")
    TSSE=edited_df

    # merge TSSE and TSSE_limit and see if the TSSE is over the limit
    TSSE_limit = pd.merge(TSSE_limit, TSSE, on='Year', how='inner')
    TSSE_limit['TSSE_over_limit'] = \
        TSSE_limit['Taxed Social Security Earnings'] - \
            TSSE_limit['Taxed_Social_Security_Earnings_Limit']
    if sum(TSSE_limit['TSSE_over_limit'] > 0) > 0:
        Years_over_limit = TSSE_limit[TSSE_limit['TSSE_over_limit'] > 0].Year
        st.text('There are some years that TSSE is over the limit.')
        st.dataframe(TSSE_limit[TSSE_limit['Year'].isin(Years_over_limit)])
        st.text('Please correct the data.')

    # print Year not in TSSE
    if sum(~TSSE.Year.dropna().isin(AWI.Year)) > 0:
        Years_not_in_TSSE = TSSE[~TSSE.Year.isin(AWI.Year)].Year
        st.text('There are some years that AWI is not provided yet')
        st.text(f'The following years will be ignored: {Years_not_in_TSSE.values}')


    st.markdown('# Output Table')
    # merge AWI and TSSE
    df = pd.merge(AWI, TSSE, on='Year', how='inner')
    # convert to the latest year value
    latest_year = df.Year.max()
    df[f'Value_{latest_year}']=df['Taxed Social Security Earnings'] / \
        df['AWI'] * df.loc[df.Year==latest_year, 'AWI'].values[0]

    # take the largest 35 TSSE_{latest_year} and then sort by Year
    Years_to_use = df.sort_values(by=f'Value_{latest_year}', ascending=False).head(35).Year
    df[f'Earnings_Value_in_{latest_year}'] = df[f'Value_{latest_year}'].where(df.Year.isin(Years_to_use), 0)

    # calculate AIME up to the year
    df['AIME_cumulative']=0.00
    for y in df.Year:
        df.loc[df.Year==y, 'AIME_cumulative'] = \
            df.loc[df.Year <= y, f'Earnings_Value_in_{latest_year}'].sum() / 12 / 35

    df['PIA_cumulative']= df['AIME_cumulative'].apply(calculate_pia)
    df=df.sort_values(by='Year', ascending=True)
    df['PIA_gain'] = df['PIA_cumulative'].diff()
    df['PIA_gain'] = df['PIA_gain'].where(pd.notna(df['PIA_gain']), df.PIA_cumulative)


    st.markdown(f'''
The following table shows the PIA growth over time.\n
**Earnings_Value_in_{latest_year}**: The above earnings were coverted to the current values. The AWI, Average Wage Index, was obtained from [here](https://www.ssa.gov/oact/cola/AWI.html))\n
**AIME_cumulative**: The AIME (Average Indexed Monthly Earnings) was calculated up to the year \n
**PIA_cumulative**: The PIA (Primary Insurance Amount) was calculated up to the year\n
**PIA_gain**: The PIA gain over time
''')

    st.dataframe(df.drop(columns=['Taxed Social Security Earnings','AWI', f'Value_{latest_year}']).style.format({
        f"Earnings_Value_in_{latest_year}": "{:.0f}".format,
        'AIME_cumulative': '{:.0f}'.format,
        'PIA_cumulative': '{:.0f}'.format,
        'PIA_gain': "{:.0f}".format,
        }))

    # plot the PIA over time
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=df['Year'],
            y=df['PIA_cumulative'],
            name="PIA grouwth over time"
        ))
    fig.add_trace(
        go.Bar(
            x=df['Year'],
            y=df['PIA_gain'],
            name="PIA gain over time"
        ))

    st.plotly_chart(fig, use_container_width=True)





if __name__ == '__main__':
    main()

