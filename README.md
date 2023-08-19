# Bayesian-Reliability-Update

1. Looping is main python file

2. Input.txt is input file consist of estimated life span by expert on first two row. Subsequent row containt Conditional State (1-4) 
of each maintenance interval. At the end of Conditional State, put -1 value to indicate an ending of input.

3. Output consist of two csv file in which finalresult1_1 and finalresult1_2.

4. finalresult1_1 contain CDF and remaining year correlation at the final year where reliability = 0.5.

5. finalresult1_2 contain estimated remaining life during reliability = 0.5, 0.6, 0.7, 0.8, 0.9. 
Row 1 to Row 5 indicating reliability of 0.5 to 0.9 respectively.
Column 1 to n indicating number of maintenance.
