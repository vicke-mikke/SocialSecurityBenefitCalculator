# calculate the PIA from AIME (defalut breakpoints from 2023)
def calculate_pia(aime, 
                  breakpoint1=1115, breakpoint2=6721, 
                  rate1=0.9, rate2=0.32, rate3=0.15):
    """
    Calculate the Primary Insurance Amount (PIA) based on the Average Indexed Monthly Earnings (AIME)
    and the breakpoints.
    
    Parameters:
    aime (float): Average Indexed Monthly Earnings
    breakpoint1 (float): First breakpoint
    breakpoint2 (float): Second breakpoint
    rate1 (float): Replacement rate for earnings up to the first breakpoint
    rate2 (float): Replacement rate for earnings between the first and second breakpoint
    rate3 (float): Replacement rate for earnings above the second breakpoint
    
    Returns:
    float: Primary Insurance Amount (PIA)
    """
    
    # Calculate the portions of AIME that fall into each bracket
    portion1 = min(aime, breakpoint1)
    portion2 = min(max(aime - breakpoint1, 0), breakpoint2 - breakpoint1)
    portion3 = max(aime - breakpoint2, 0)
    
    # Calculate PIA
    pia = (portion1 * rate1) + (portion2 * rate2) + (portion3 * rate3)
    
    return pia