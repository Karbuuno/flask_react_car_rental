from backend import create_app, mongo
from backend.data.cars import car_data
def seed_cars():
    app = create_app()
    with app.app_context():
        cars = mongo.db.cars
        cars.delete_many({})  # clear old data
        cars.insert_many(car_data)
        print(f"✅ Seeded {len(car_data)} cars successfully!")

if __name__ == "__main__":
    seed_cars()
