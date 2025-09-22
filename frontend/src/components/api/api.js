import { data } from "autoprefixer";
import axios from "axios";

export const login = async (inputs) => {
  try {
    const { data } = await axios.post("/api/users/auth", inputs, {
      headers: {
        "content-type": "application/json",
      },
    });

    return data;
  } catch (error) {
    console.log(error);
  }
};

export const register = async (inputs) => {
  try {
    const res = await axios.post("/api/users/", inputs, {
      headers: {
        "Content-Type": "application/json",
      },
      withCredentials: true,
    });

    return res.data;
  } catch (error) {
    throw error.response?.data || error;
  }
};

export const logout = async (inputs) => {
  try {
    const res = await axios.post("/api/users/logout");

    // const token = res?.data?.token'

    return res.data;
  } catch (error) {
    console.log(error);
  }
};

//all cars
export const allCarsData = async () => {
  const { data } = await axios.get("/api/cars");
  return data;
};
//single car
export const carDetails = async (car_id) => {
  const { data } = await axios.get(`/api/cars/${car_id}`);

  return data;
};
// register a car
export const addCar = async (FormData) => {
  const { data } = await axios.post("/api/cars/add_car", FormData, {
    headers: { "Content-Type": "multipart/form-data" },
  });
  console.log(data);
  return data;
};

//search car details
export const SearchCarsData = async (location) => {
  const { data } = await axios.get(`/api/cars/search/${location}`);
  return data;
};

// stripe api
export const checkout = async (stripeData) => {
  try {
    const { data } = await axios.post(
      "/api/stripe/create_checkout_session",
      stripeData,
      {
        headers: {
          "content-type": "application/json",
        },
      },
      {
        withCredentials: true, // if using cookies / JWT
      }
    );
    if (data) {
      window.location.href = data.url;
    }
    return data;
  } catch (error) {
    console.log(error.message);
  }
};

//Update car
export const updateCar = async (_id, formData) => {
  const { data } = await axios.put(`/api/cars/update/${_id}`, formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });
  console.log(data);
  return data;
};

export const updateProfile = async (updatedUser) => {
  const { data } = await axios.put(`/api/users/profile`, updatedUser, {
    headers: { "Content-Type": "application/json" },
  });
  return data;
};

// Delete car
export const deleteCar = async (car_id) => {
  const { data } = await axios.delete(`/api/cars/delete/${car_id}`);
  return data;
};
export const carAvailable = async (id) => {
  const { data } = await axios.patch(`/api/cars/available/${id}`, {
    headers: {
      "content-type": "application/json",
    },
  });
  return data;
};

// user bookings
export const userBookings = async () => {
  const { data } = await axios.get("/api/bookings/myBookings");
  return data;
};
export const allBookings = async () => {
  const { data } = await axios.get("/api/bookings/");
  return data;
};

//delete booking
export const deleteBooking = async (id) => {
  const { data } = await axios.delete(`/api/bookings/delete-booking/${id}`);
  return data;
};
