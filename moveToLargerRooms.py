import pandas as pd
class moveToLargerRooms:
    def optimize_room_assignments(possible_schedule_path, room_capacities_path):
        
        exam_schedule = pd.read_excel(possible_schedule_path)
        room_capacities = pd.read_excel(room_capacities_path)

        
        room_capacities.rename(columns={'ROOM NAME': 'Room', 'CAPACITY': 'Capacity'}, inplace=True)

        # Initialize updated exams list
        updated_exams = []

        for newtime in exam_schedule['NewTime'].unique():
            # Extract exams for this NewTime
            exams_at_newtime = exam_schedule[exam_schedule['NewTime'] == newtime]

            available_rooms = room_capacities.copy()
            available_rooms.sort_values(by='Capacity', ascending=False, inplace=True)

            for _, exam in exams_at_newtime.iterrows():
                original_room = exam['Final Exam Room']  # Store the original room
                for idx, room in available_rooms.iterrows():
                    if room['Capacity'] >= exam['Count']:
                        exam['New Assigned Room'] = room['Room']  # Assign a new room
                        available_rooms.drop(idx, inplace=True)  # Remove the assigned room
                        break
                    else:
                        exam['New Assigned Room'] = original_room  # Keep the original room if no suitable room found

                updated_exams.append(exam)


        updated_exam_schedule = pd.DataFrame(updated_exams)

    
        final_sorted_schedule = updated_exam_schedule.sort_values(by='Count', ascending=False)

    
        final_sorted_schedule.to_excel("updated_room_schedule.xlsx", index=False)

        return final_sorted_schedule
