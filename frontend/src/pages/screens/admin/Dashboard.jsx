import React, { useState } from "react";
import dayjs from "dayjs";
import {
  Table,
  TableBody,
  TableCaption,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { useMutation, useQuery, useQueryClient } from "react-query";
import {
  deleteCar,
  allBookings,
  allCarsData,
  carAvailable,
  deleteBooking,
} from "@/components/api/api";
import { bookingStatus } from "@/components/api/daysDiff";
import CarFormDialog from "@/components/CarFormDialog"; // ✅ Reusable Add/Edit Car form

function AdminDashboard() {
  const [activeTab, setActiveTab] = useState("allCars");

  const { data: carData } = useQuery("cars", allCarsData);
  const {
    data: bookings,
    error,
    isLoading,
  } = useQuery("bookings", allBookings);

  const queryClient = useQueryClient();

  const carAvailableMutation = useMutation({
    mutationFn: carAvailable,
    onSuccess: () => {
      queryClient.invalidateQueries("bookings");
      queryClient.invalidateQueries("cars");
    },
  });

  const deleteCarMutation = useMutation({
    mutationFn: deleteCar,
    onSuccess: () => {
      queryClient.invalidateQueries("cars");
    },
  });

  const deleteBookingMutation = useMutation({
    mutationFn: deleteBooking,
    onSuccess: () => {
      queryClient.invalidateQueries("bookings");
      queryClient.invalidateQueries("cars");
    },
  });

  // Separate handlers
  const handleDeleteCar = (id) => deleteCarMutation.mutate(id);
  const handleDeleteBooking = (id) => deleteBookingMutation.mutate(id);

  // Filter data by tab
  const filteredData = (() => {
    if (activeTab === "activeBookings")
      return bookings?.filter((b) => !b.isAvailable);
    if (activeTab === "allCars") return carData;
    if (activeTab === "allBookings") return bookings;
    if (activeTab === "availableCars")
      return carData?.filter((c) => c.isAvailable);
    return [];
  })();

  return (
    <div className="max-w-6xl mx-auto mt-16 px-4 sm:px-6">
      <h1 className="text-2xl sm:text-3xl font-bold mb-6">
        📊 Admin Dashboard
      </h1>

      {/* Tabs */}
      <div className="flex flex-wrap gap-2 sm:gap-4 mb-8">
        {[
          { key: "allCars", label: "All Cars" },
          { key: "availableCars", label: "Available Cars" },
          { key: "allBookings", label: "All Bookings" },
          { key: "activeBookings", label: "Active Bookings" },
        ].map((tab) => (
          <button
            key={tab.key}
            onClick={() => setActiveTab(tab.key)}
            className={`px-3 sm:px-4 py-2 rounded-lg text-sm sm:text-base ${
              activeTab === tab.key ? "bg-blue-500 text-white" : "bg-gray-200"
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      <div className="bg-white shadow-lg rounded-2xl">
        {isLoading ? (
          <p className="p-6 text-lg">Loading...</p>
        ) : error ? (
          <p className="p-6 text-red-500">Failed to fetch data</p>
        ) : (
          <>
            {/* Add Car button for All Cars */}
            {activeTab === "allCars" && (
              <div className="flex justify-end p-4">
                <CarFormDialog buttonTitle="➕ Add Car" />
              </div>
            )}

            {/* Table for md+ */}
            <div className="hidden md:block overflow-x-auto">
              <Table>
                <TableCaption>
                  {activeTab.includes("Bookings")
                    ? `Recent Bookings (${filteredData?.length || 0})`
                    : `Cars (${filteredData?.length || 0})`}
                </TableCaption>

                <TableHeader className="bg-gray-100">
                  <TableRow>
                    {activeTab.includes("Bookings") ? (
                      <>
                        <TableHead>Reg Number</TableHead>
                        <TableHead>Car Make</TableHead>
                        <TableHead>Start Date</TableHead>
                        <TableHead>End Date</TableHead>
                        <TableHead>Amount</TableHead>
                        <TableHead>Status</TableHead>
                        <TableHead>Action</TableHead>
                      </>
                    ) : (
                      <>
                        <TableHead>Reg Number</TableHead>
                        <TableHead>Car Name</TableHead>
                        <TableHead>Car Type</TableHead>
                        <TableHead>Seats</TableHead>
                        <TableHead>Location</TableHead>
                        <TableHead>Price</TableHead>
                        <TableHead>Available</TableHead>
                        <TableHead>Action</TableHead>
                      </>
                    )}
                  </TableRow>
                </TableHeader>

                <TableBody>
                  {activeTab.includes("Bookings")
                    ? filteredData?.map((booking) => (
                        <TableRow key={booking._id}>
                          <TableCell>{booking.regNumber}</TableCell>
                          <TableCell>{booking.make}</TableCell>
                          <TableCell>
                            {dayjs(booking.startDate).format("DD/MM/YYYY")}
                          </TableCell>
                          <TableCell>
                            {dayjs(booking.endDate).format("DD/MM/YYYY")}
                          </TableCell>
                          <TableCell>£{booking.totalPrice}</TableCell>
                          <TableCell>
                            <span
                              className={`block text-center px-3 py-1 w-[140px] rounded-md text-sm font-semibold ${
                                bookingStatus(booking.endDate).includes("Ended")
                                  ? "bg-red-200 text-red-800"
                                  : "bg-yellow-200 text-yellow-800"
                              }`}
                            >
                              {bookingStatus(booking.endDate)}
                            </span>
                          </TableCell>
                          <TableCell>
                            {!booking.isAvailable ? (
                              <button
                                onClick={() => handleAvailable(booking._id)}
                                className="block text-center px-3 py-1 w-[140px] rounded-lg bg-blue-500 text-white hover:bg-blue-600"
                              >
                                Mark Available
                              </button>
                            ) : (
                              <button
                                onClick={() => handleDeleteBooking(booking._id)}
                                className="block text-center px-3 py-1 w-[140px] rounded-lg bg-red-500 text-white hover:bg-red-600"
                              >
                                Delete
                              </button>
                            )}
                          </TableCell>
                        </TableRow>
                      ))
                    : filteredData?.map((car) => (
                        <TableRow key={car._id}>
                          <TableCell>{car.regNumber}</TableCell>
                          <TableCell>{car.name}</TableCell>
                          <TableCell>{car.carType}</TableCell>
                          <TableCell>{car.seats}</TableCell>
                          <TableCell>{car.location}</TableCell>
                          <TableCell>£{car.price}</TableCell>
                          <TableCell>
                            {car.isAvailable ? (
                              <span className="text-green-600 font-semibold">
                                Yes
                              </span>
                            ) : (
                              <span className="text-red-600 font-semibold">
                                No
                              </span>
                            )}
                          </TableCell>
                          <TableCell className="flex gap-2">
                            <CarFormDialog buttonTitle="Edit" carToEdit={car} />
                            <button
                              onClick={() => handleDeleteCar(car._id)}
                              className="px-3 py-1 w-[100px] rounded-lg bg-red-500 text-white hover:bg-red-600"
                            >
                              Delete
                            </button>
                          </TableCell>
                        </TableRow>
                      ))}
                </TableBody>
              </Table>
            </div>

            {/* Mobile cards */}
            <div className="md:hidden divide-y">
              {activeTab.includes("Bookings")
                ? filteredData?.map((booking) => (
                    <div
                      key={booking._id}
                      className="p-4 grid grid-cols-2 gap-y-2 gap-x-4"
                    >
                      <div className="font-semibold">Car</div>
                      <div>
                        {booking.make} ({booking.regNumber})
                      </div>

                      <div className="font-semibold">Start</div>
                      <div>{dayjs(booking.startDate).format("DD/MM/YYYY")}</div>

                      <div className="font-semibold">End</div>
                      <div>{dayjs(booking.endDate).format("DD/MM/YYYY")}</div>

                      <div className="font-semibold">Amount</div>
                      <div>£{booking.totalPrice}</div>

                      <div className="font-semibold">Status</div>
                      <div>
                        <span
                          className={`block text-center px-3 py-1 w-[140px] rounded-md text-sm font-semibold ${
                            bookingStatus(booking.endDate).includes("Ended")
                              ? "bg-red-200 text-red-800"
                              : "bg-yellow-200 text-yellow-800"
                          }`}
                        >
                          {bookingStatus(booking.endDate)}
                        </span>
                      </div>

                      <div className="col-span-2 pt-2 flex justify-center">
                        {!booking.isAvailable ? (
                          <button
                            onClick={() => handleAvailable(booking._id)}
                            className="block text-center px-3 py-2 w-[140px] rounded-lg bg-blue-500 text-white hover:bg-blue-600"
                          >
                            Mark Available
                          </button>
                        ) : (
                          <button
                            onClick={() => handleDeleteBooking(booking._id)}
                            className="block text-center px-3 py-2 w-[140px] rounded-lg bg-red-500 text-white hover:bg-red-600"
                          >
                            Delete
                          </button>
                        )}
                      </div>
                    </div>
                  ))
                : filteredData?.map((car) => (
                    <div
                      key={car._id}
                      className="p-4 grid grid-cols-2 gap-y-2 gap-x-4"
                    >
                      <div className="font-semibold">Reg Number</div>
                      <div>{car.regNumber}</div>

                      <div className="font-semibold">Name</div>
                      <div>{car.name}</div>

                      <div className="font-semibold">Type</div>
                      <div>{car.carType}</div>

                      <div className="font-semibold">Seats</div>
                      <div>{car.seats}</div>

                      <div className="font-semibold">Location</div>
                      <div>{car.location}</div>

                      <div className="font-semibold">Price</div>
                      <div>£{car.price}</div>

                      <div className="font-semibold">Available</div>
                      <div>
                        {car.isAvailable ? (
                          <span className="text-green-600 font-semibold">
                            Yes
                          </span>
                        ) : (
                          <span className="text-red-600 font-semibold">No</span>
                        )}
                      </div>

                      <div className="col-span-2 flex gap-2 pt-2 justify-center">
                        <CarFormDialog buttonTitle="Edit" carToEdit={car} />
                        <button
                          onClick={() => handleDeleteCar(car._id)}
                          className="block text-center px-3 py-2 w-[140px] rounded-lg bg-red-500 text-white hover:bg-red-600"
                        >
                          Delete
                        </button>
                      </div>
                    </div>
                  ))}
            </div>
          </>
        )}
      </div>
    </div>
  );
}

export default AdminDashboard;
