import pandas
import matplotlib.pyplot as plot

# Paths can be modified if necessary
world_path = "owid-covid-latest.csv"
state_path = "us-states.csv"
county_path = "us-counties.csv"


# World COVID data from Our World In Data, US state and county data from The New York Times
# The program starts up here, prompting the user for inputs
def get_user_response():
    data_type = input("Do you want to compare counties, states, or countries?\n")
    # Converts the input to lowercase
    if data_type.lower() == "counties":
        # Proper input format is very important, program will error out otherwise
        first_response = input("Enter your first county in county, state format. Example: Union, New Jersey:\n")
        second_response = input("Enter your second county:\n")

        # Stripping out the space in the input so the state can be properly matched later
        first_county = first_response.split(",")
        first_county[1] = first_county[1].strip()

        second_county = second_response.split(",")
        second_county[1] = second_county[1].strip()

        # Labels are for the bar plots
        cases, deaths, labels = get_county_data(first_county, second_county)
        plot_data(cases, deaths, labels)

    elif data_type.lower() == "states":
        first_response = input("Enter your first state:\n")
        second_response = input("Enter your second state:\n")

        # Different function for each data type because of differences in the files and inputs
        cases, deaths, labels = get_state_data(first_response, second_response)
        plot_data(cases, deaths, labels)

    elif data_type.lower() == "countries":
        first_response = input("Enter your first country:\n")
        second_response = input("Enter your second country:\n")

        cases, deaths, labels = get_world_data(first_response, second_response)
        plot_data(cases, deaths, labels)

    else:
        print("Invalid input")


def get_world_data(first_country, second_country):
    # Using Pandas to extract the data from the CSV file
    world_data = pandas.read_csv(world_path)

    # DataFrame.loc function returns rows that match the criteria in brackets
    # Because we only have one row of data, we can use the squeeze function to reduce into a Series
    # Series.array reduces the Series into a Pandas array we can extract the raw data from
    first_data = world_data.loc[world_data["location"] == first_country].squeeze().array
    second_data = world_data.loc[world_data["location"] == second_country].squeeze().array

    # Cases are at index 4 in the CSV file, deaths are at index 6
    cases = [int(first_data[4]), int(second_data[4])]
    deaths = [int(first_data[6]), int(second_data[6])]
    labels = [first_country, second_country]
    return cases, deaths, labels


def get_state_data(first_state, second_state):
    state_data = pandas.read_csv(state_path)
    first_data = state_data.loc[state_data["state"] == first_state].squeeze().array
    second_data = state_data.loc[state_data["state"] == second_state].squeeze().array

    # Cases are at index 3 in the CSV file, deaths are at index 4
    cases = [first_data[3], second_data[3]]
    deaths = [first_data[4], second_data[4]]
    labels = [first_state, second_state]
    return cases, deaths, labels


def get_county_data(first_county, second_county):
    # Inputs are of the form [county, state] so counties can be uniquely identified
    county_data = pandas.read_csv(county_path)

    # Narrowing the data by state first, then county to ensure we only get one row of data
    first_data_init = county_data.loc[county_data["state"] == first_county[1]]
    first_data = first_data_init.loc[county_data["county"] == first_county[0]].squeeze().array

    second_data_init = county_data.loc[county_data["state"] == second_county[1]]
    second_data = second_data_init.loc[county_data["county"] == second_county[0]].squeeze().array

    # Cases are at index 4 in the CSV file, deaths are at index 5
    cases = [first_data[4], second_data[4]]
    deaths = [first_data[5], second_data[5]]

    # Constructing the label strings so that the final chart will say "X County, State" instead of "X, State"
    first_county_string = first_county[0] + " County, " + first_county[1]
    second_county_string = second_county[0] + " County, " + second_county[1]
    labels = [first_county_string, second_county_string]
    return cases, deaths, labels


def plot_data(cases, deaths, labels):
    # Creating bar charts to compare the total cases and deaths
    plot.bar(range(len(cases)), cases, color="green")
    plot.ticklabel_format(style="plain")
    plot.xticks(range(len(cases)), labels)
    plot.xlabel("Total cases of COVID-19")
    plot.show()

    plot.bar(range(len(deaths)), deaths, color="red")
    plot.ticklabel_format(style="plain")
    plot.xticks(range(len(deaths)), labels)
    plot.xlabel("Total deaths from COVID-19")
    plot.show()


# Running the main function
get_user_response()
