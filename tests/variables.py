
list1 = [4, 5, 6]
list2 = [1, 2, 3]

list3 = [list1, list2]

print(sum(sum(l) for l in list3))



# art_test_input = input("Are you ART positive? (y/n) ")
# if art_test_input == "y":
#     day_input = int(input("number of days ART positive: "))

#     if day_input >= 7:
#         print("No ART test is required student may return to campus.")
#     elif day_input == 4:
#         feeling_well = input("Are you feeling well? (y/n) ")
#         if feeling_well == "y":
#             print("You may return to school but must exercise discretion by minimising close physical contact with others and wearing a mask.")
#         elif feeling_well == "n":
#             print("Please remain on LOA and encouraged to see a doctor")
#     elif day_input <= 3:
#         print("You are still on LOA")

# elif art_test_input == "n":
#     print("You may return to campus.")
