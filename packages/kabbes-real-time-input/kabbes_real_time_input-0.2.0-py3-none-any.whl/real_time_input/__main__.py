import real_time_input

RTI = real_time_input.RealTimeInput()

print ('Type to add words to your selection: ')
RTI.get_multiple_inputs()
print ()
print ('Selections: ' + str(RTI.selections))
print ('Final Input: ' + RTI.string)