from apis.flip import fl
from apis.ama import amazon

def compare_p(name):
    fprice = fl(name)
    amprice = amazon(name)
    
    if amprice[0] != '₹':
        amprice = "₹" + amprice
    # Extract numerical values from strings, ignoring the currency symbol and any other characters
    fprice_value = float(''.join(filter(str.isdigit, fprice)))
    amprice_value = float(''.join(filter(str.isdigit, amprice)))
    
    # Check if any of the prices is zero
    if fprice_value == 0:
        return "Price on Flipkart is not available.\nPrice on Amazon is " + amprice
    elif amprice_value == 0:
        return "Price on Amazon is not available.\nPrice on Flipkart is " + fprice
    
    comparison_result = "Price on Flipkart is " + fprice + "\nPrice on Amazon is " + amprice
    
    return comparison_result

# Example usage
# name = input("Enter product name: ")
# comparison = compare_p(name)
# print(comparison)