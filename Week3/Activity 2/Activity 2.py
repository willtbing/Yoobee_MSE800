filename = "/Users/wupei/Documents/GitHub/YoobeeMSE800/Week3/Activity 2/junk.txt"
#Open, read, and process the attached data file. 
with open(filename, "r") as data:
    lines = data.readlines()
#Calculate and report the total number of lines in the file.
print("The total number of lines in the file.")
print(len(lines))
#Add a new line at the end of the file containing exactly: `text file nanalyssis`
text = ''.join(lines)
print("------------------------------------")
print("The original data:")
print(text)
text += "text file nanalyssis\n"
with open(filename, "w") as data:
    data.write(text)
print("------------------------------------")
print("The updated data after adding one more record:")
print(text)
#Convert all text in the `junk.txt` file to lowercase.
text = text.lower()
with open(filename, "w") as data:
    data.write(text)
print("------------------------------------")
print("The updated data after converting to lowercase:")
print(text)
data.close()
