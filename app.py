from flask import Flask, request, render_template
from flask_cors import cross_origin
import pickle
import sklearn
import pandas as pd

app = Flask(__name__)
model = pickle.load(open('flight_rf.pkl', 'rb'))

@app.route("/")
@cross_origin()

def home(): 
    return render_template('home.html')


@app.route("/predict", methods = ['GET', 'POST'])
@cross_origin()

def predict(): 
    if request.method == 'POST': 

        # Date of Journey
        date_dep = request.form["Dep_Time"]
        Journey_day = int(pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M").day)
        Journey_month = int(pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M").month)
        # print("Journey Date : ",Journey_day, Journey_month)

        # Departure
        Dep_hour = int(pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M").hour)
        Dep_min = int(pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M").minute)
        # print("Departure : ",Dep_hour, Dep_min)

        # Arrival
        date_arr = request.form["Arrival_Time"]
        Arrival_hour = int(pd.to_datetime(date_arr, format="%Y-%m-%dT%H:%M").hour)
        Arrival_min = int(pd.to_datetime(date_arr, format="%Y-%m-%dT%H:%M").minute)
        # print("Arrival : ", Arrival_hour, Arrival_min)

        # Duration
        dur_hour = abs(Arrival_hour - Dep_hour)
        dur_min = abs(Arrival_min - Dep_min)
        # print("Duration : ", dur_hour, dur_min)

        # Total Stops
        Total_stops = int(request.form["stops"])
        # print(Total_stops)

        # Is Weekend
        Weekday = str(pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M").strftime('%A'))
        if Weekday in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']: 
            is_Weekend = 0
        else: 
            is_Weekend = 1

        # Additional Info
        Additional_Info = request.form['Additional_Info']
        if Additional_Info == 'In-flight meal not included': 
            in_flight_meal_not_included = 1
            no_check_in_baggage_included = 0
            one_long_layover = 0
            change_airports = 0
            business_class = 0
            one_short_layover = 0
            red_eye_flight = 0
            two_long_layover = 0

        elif Additional_Info == 'No Check In Baggage Included': 
            in_flight_meal_not_included = 0
            no_check_in_baggage_included = 1
            one_long_layover = 0
            change_airports = 0
            business_class = 0
            one_short_layover = 0
            red_eye_flight = 0
            two_long_layover = 0

        elif Additional_Info == 'One Long Layover': 
            in_flight_meal_not_included = 0
            no_check_in_baggage_included = 0
            one_long_layover = 1
            change_airports = 0
            business_class = 0
            one_short_layover = 0
            red_eye_flight = 0
            two_long_layover = 0

        elif Additional_Info == 'Change Airports': 
            in_flight_meal_not_included = 0
            no_check_in_baggage_included = 0
            one_long_layover = 0
            change_airports = 1
            business_class = 0
            one_short_layover = 0
            red_eye_flight = 0
            two_long_layover = 0

        elif Additional_Info == 'Business Class': 

            in_flight_meal_not_included = 0
            no_check_in_baggage_included = 0
            one_long_layover = 0
            change_airports = 0
            business_class = 1
            one_short_layover = 0
            red_eye_flight = 0
            two_long_layover = 0

        elif Additional_Info == 'One Short Layover': 
            in_flight_meal_not_included = 0
            no_check_in_baggage_included = 0
            one_long_layover = 0
            change_airports = 0
            business_class = 0
            one_short_layover = 1
            red_eye_flight = 0
            two_long_layover = 0

        elif Additional_Info == 'Red Eye Flight': 
            in_flight_meal_not_included = 0
            no_check_in_baggage_included = 0
            one_long_layover = 0
            change_airports = 0
            business_class = 0
            one_short_layover = 0
            red_eye_flight = 1
            two_long_layover = 0

        elif Additional_Info == 'Two Long Layovers': 
            in_flight_meal_not_included = 0
            no_check_in_baggage_included = 0
            one_long_layover = 0
            change_airports = 0
            business_class = 0
            one_short_layover = 0
            red_eye_flight = 0
            two_long_layover = 1

        else: 
            in_flight_meal_not_included = 0
            no_check_in_baggage_included = 0
            one_long_layover = 0
            change_airports = 0
            business_class = 0
            one_short_layover = 0
            red_eye_flight = 0
            two_long_layover = 0

        # Airline
        # AIR ASIA = 0 (not in column)
        airline = request.form['airline']
        if airline == 'Jet Airways':
            Jet_Airways = 1
            IndiGo = 0
            Air_India = 0
            Multiple_carriers = 0
            SpiceJet = 0
            Vistara = 0
            GoAir = 0
            Trujet = 0

        elif airline == 'IndiGo':
            Jet_Airways = 0
            IndiGo = 1
            Air_India = 0
            Multiple_carriers = 0
            SpiceJet = 0
            Vistara = 0
            GoAir = 0
            Trujet = 0

        elif airline == 'Air India':
            Jet_Airways = 0
            IndiGo = 0
            Air_India = 1
            Multiple_carriers = 0
            SpiceJet = 0
            Vistara = 0
            GoAir = 0
            Trujet = 0

        elif airline == 'Multiple carriers':
            Jet_Airways = 0
            IndiGo = 0
            Air_India = 0
            Multiple_carriers = 1
            SpiceJet = 0
            Vistara = 0
            GoAir = 0
            Trujet = 0

        elif airline == 'SpiceJet':
            Jet_Airways = 0
            IndiGo = 0
            Air_India = 0
            Multiple_carriers = 0
            SpiceJet = 1
            Vistara = 0
            GoAir = 0
            Trujet = 0

        elif airline == 'Vistara':
            Jet_Airways = 0
            IndiGo = 0
            Air_India = 0
            Multiple_carriers = 0
            SpiceJet = 0
            Vistara = 1
            GoAir = 0
            Trujet = 0

        elif airline == 'GoAir':
            Jet_Airways = 0
            IndiGo = 0
            Air_India = 0
            Multiple_carriers = 0
            SpiceJet = 0
            Vistara = 0
            GoAir = 1
            Trujet = 0

        else:
            Jet_Airways = 0
            IndiGo = 0
            Air_India = 0
            Multiple_carriers = 0
            SpiceJet = 0
            Vistara = 0
            GoAir = 0
            Trujet = 0

        # print(Jet_Airways,
        #     IndiGo,
        #     Air_India,
        #     Multiple_carriers,
        #     SpiceJet,
        #     Vistara,
        #     GoAir,
        #     Multiple_carriers_Premium_economy,
        #     Jet_Airways_Business,
        #     Vistara_Premium_economy,
        #     Trujet)

        # Source
        # Banglore = 0 (not in column)
        Source = request.form["Source"]
        if Source == 'Delhi':
            s_Delhi = 1
            s_Kolkata = 0
            s_Mumbai = 0
            s_Chennai = 0

        elif Source == 'Kolkata':
            s_Delhi = 0
            s_Kolkata = 1
            s_Mumbai = 0
            s_Chennai = 0

        elif Source == 'Mumbai':
            s_Delhi = 0
            s_Kolkata = 0
            s_Mumbai = 1
            s_Chennai = 0

        elif (Source == 'Chennai'):
            s_Delhi = 0
            s_Kolkata = 0
            s_Mumbai = 0
            s_Chennai = 1

        else:
            s_Delhi = 0
            s_Kolkata = 0
            s_Mumbai = 0
            s_Chennai = 0

        # print(s_Delhi,
        #     s_Kolkata,
        #     s_Mumbai,
        #     s_Chennai)

        # Destination
        # Banglore = 0 (not in column)
        Source = request.form["Destination"]
        if Source == 'Cochin':
            d_Cochin = 1
            d_Delhi = 0
            d_Hyderabad = 0
            d_Kolkata = 0

        elif Source == 'Delhi':
            d_Cochin = 0
            d_Delhi = 1
            d_Hyderabad = 0
            d_Kolkata = 0

        elif Source == 'Hyderabad':
            d_Cochin = 0
            d_Delhi = 0
            d_Hyderabad = 1
            d_Kolkata = 0

        elif Source == 'Kolkata':
            d_Cochin = 0
            d_Delhi = 0
            d_Hyderabad = 0
            d_Kolkata = 1

        else:
            d_Cochin = 0
            d_Delhi = 0
            d_Hyderabad = 0
            d_Kolkata = 0

        # print(
        #     d_Cochin,
        #     d_Delhi,
        #     d_New_Delhi,
        #     d_Hyderabad,
        #     d_Kolkata
        # )

        #     ['Total_Stops', 'Journey_day', 'Journey_month', 'Dep_hour',
        #    'Dep_min', 'Arrival_hour', 'Arrival_min', 'Duration_hours',
        #    'Duration_mins', 'Airline_Air India', 'Airline_GoAir', 'Airline_IndiGo',
        #    'Airline_Jet Airways', 'Airline_Jet Airways Business',
        #    'Airline_Multiple carriers',
        #    'Airline_Multiple carriers Premium economy', 'Airline_SpiceJet',
        #    'Airline_Trujet', 'Airline_Vistara', 'Airline_Vistara Premium economy',
        #    'Source_Chennai', 'Source_Delhi', 'Source_Kolkata', 'Source_Mumbai',
        #    'Destination_Cochin', 'Destination_Delhi', 'Destination_Hyderabad',
        #    'Destination_Kolkata', 'Destination_New Delhi']

        prediction = model.predict([[
            Total_stops, 
            is_Weekend, 
            Dep_hour, 
            Dep_min, 
            Arrival_hour, 
            Arrival_min, 
            Journey_day, 
            Journey_month, 
            dur_hour, 
            dur_min, 
            Jet_Airways, 
            IndiGo, 
            Air_India, 
            Multiple_carriers, 
            SpiceJet, 
            Vistara, 
            GoAir, 
            Trujet, 
            s_Delhi, 
            s_Chennai, 
            s_Kolkata, 
            s_Mumbai, 
            d_Cochin, 
            d_Delhi, 
            d_Hyderabad, 
            d_Kolkata, 
            in_flight_meal_not_included, 
            no_check_in_baggage_included, 
            one_long_layover, 
            change_airports, 
            business_class, 
            one_short_layover, 
            red_eye_flight, 
            two_long_layover
        ]])

        output = round(prediction[0], 2)

        return render_template('home.html', prediction_text="Your Flight price is Rs. {}".format(output))

    return render_template("home.html")


if __name__ == "__main__":
    app.run(debug=True)