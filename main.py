import click
import json


# Define a function to generate a workout plan
def generate_workout(age, sex, weight, height, diet, days_per_week, workout_data):
    try:
        workout_plans = workout_data.get("workout_plans", [])
        chosen_plan = None

        # Find a plan that matches the user's input
        for plan in workout_plans:
            if (
                    plan["days_per_week"] == days_per_week
                    and plan["difficulty"].lower() in ["easy", "moderate", "hard"]
                    and diet.lower() in ["veg", "non-veg"]
            ):
                chosen_plan = plan
                break

        if chosen_plan is None:
            raise click.ClickException("No suitable workout plan found based on input.")

        # Build the workout plan message
        plan = f"Workout plan for {days_per_week} days per week (Chosen Plan: {chosen_plan['name']} - {chosen_plan['difficulty']}):\n"

        for exercise in chosen_plan['exercises']:
            plan += f"{exercise['name']} - {exercise['sets']} sets x {exercise['reps']} reps\n"

        diet_recommendation = chosen_plan[diet.lower() + '_diet']

        plan += f"\nAge: {age} years\n"
        plan += f"Sex: {sex}\n"
        plan += f"Weight: {weight} kg\n"
        plan += f"Height: {height} cm\n"
        plan += diet_recommendation + "\n"

        return plan
    except Exception as e:
        raise click.ClickException(f"An error occurred: {str(e)}")


@click.command()
@click.option('--age', type=int, prompt='Your age', help='Your age')
@click.option('--sex', type=click.Choice(['male', 'female']), prompt='Your sex', help='Your sex')
@click.option('--weight', type=float, prompt='Your weight (in kg)', help='Your weight')
@click.option('--height', type=float, prompt='Your height (in cm)', help='Your height')
@click.option('--diet', type=click.Choice(['veg', 'non-veg']), prompt='Your diet (veg or non-veg)', help='Your diet')
@click.option('--days_per_week', type=int, prompt='Days available for workout per week',
              help='Days available for workout per week')
def cli(age, sex, weight, height, diet, days_per_week):
    try:
        # Load workout data from the JSON file
        with open('workout_plans.json', 'r') as file:
            workout_data = json.load(file)

        # Generate the workout plan
        workout_plan = generate_workout(age, sex, weight, height, diet, days_per_week, workout_data)
        click.echo(workout_plan)
    except click.ClickException as e:
        click.echo(e)
    except FileNotFoundError:
        click.echo("Error: JSON file 'workout_plans.json' not found")


if __name__ == '__main__':
    cli()
