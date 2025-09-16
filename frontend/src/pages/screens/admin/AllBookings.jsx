import React from "react";
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
import { MdDelete } from "react-icons/md";
import { useMutation, useQuery, useQueryClient } from "react-query";
import {
  allBookings,
  allCarsData,
  carAvailable,
  deleteBooking,
} from "@/components/api/api";

import { bookingStatus } from "@/components/api/daysDiff";

function AllBookings() {
  const { data: carData } = useQuery("cars", allCarsData);
  const { data, error, isLoading } = useQuery("bookings", allBookings);

  // console.log(carData?.filter(car => car.isAvailable).length)
  const queryClient = useQueryClient();

  const today = dayjs();
  // const currentDate = today.format("DD/MM/YYYY");

  const carAvailableMutation = useMutation({
    mutationFn: carAvailable,
    onSuccess: () => {
      queryClient.invalidateQueries("bookings");
    },
  });

  const deleteBookingMutation = useMutation({
    mutationFn: deleteBooking,
    onSuccess: () => {
      queryClient.invalidateQueries("bookings");
    },
  });

  const handleDelete = (id) => deleteBookingMutation.mutate(id);
  const handleAvailable = (id) => carAvailableMutation.mutate(id);

  return (
    <div className="max-w-6xl mx-auto mt-16 px-6">
      <h1 className="text-3xl font-bold mb-6">📊 Admin Bookings Dashboard</h1>

      {/* Stats Overview */}
      {data && (
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-6 mb-8">
          <div className="bg-blue-100 p-4 rounded-2xl shadow text-center">
            <h3 className="text-lg font-semibold">Total Bookings</h3>
            <p className="text-2xl font-bold">{data.length}</p>
          </div>
          <div className="bg-green-100 p-4 rounded-2xl shadow text-center">
            <h3 className="text-lg font-semibold">Active Bookings</h3>
            <p className="text-2xl font-bold">
              {data?.filter((b) => !b.isAvailable).length}
            </p>
          </div>
          {carData && (
            <div className="bg-gray-100 p-4 rounded-2xl shadow text-center">
              <h3 className="text-lg font-semibold">Available Cars</h3>
              <p className="text-2xl font-bold">
                {carData?.filter((car) => car.isAvailable).length}
              </p>
            </div>
          )}
        </div>
      )}

      {/* Bookings Table */}
      <div className="bg-white shadow-lg rounded-2xl">
        {isLoading ? (
          <p className="p-6 text-lg">Loading bookings...</p>
        ) : error ? (
          <p className="p-6 text-red-500">Failed to fetch data</p>
        ) : (
          <>
            {/* Table for larger screens */}
            <div className="hidden md:block overflow-x-auto">
              <Table>
                <TableCaption>Recent Bookings</TableCaption>
                <TableHeader className="bg-gray-100">
                  <TableRow>
                    <TableHead>Reg Number</TableHead>
                    <TableHead>Car Make</TableHead>
                    <TableHead>Start Date</TableHead>
                    <TableHead>End Date</TableHead>
                    <TableHead>Amount</TableHead>
                    <TableHead>Status</TableHead>
                    <TableHead>Action</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {data?.map((booking) => (
                    <TableRow key={booking._id} className="hover:bg-gray-50">
                      <TableCell>{booking.regNumber}</TableCell>
                      <TableCell>{booking.make}</TableCell>
                      <TableCell>
                        {dayjs(booking.startDate).format("DD/MM/YYYY")}
                      </TableCell>
                      <TableCell>
                        {dayjs(booking.endDate).format("DD/MM/YYYY")}
                      </TableCell>
                      <TableCell>
                        <span className="font-bold">£</span>
                        {booking.totalPrice}
                      </TableCell>
                      <TableCell>
                        <span
                          className={`md:block px-3 py-1 rounded-md font-semibold ${
                            bookingStatus(booking.endDate).includes("Ended")
                              ? "bg-red-200 text-red-800"
                              : bookingStatus(booking.endDate).includes("today")
                              ? "bg-yellow-200 text-yellow-800"
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
                            className="px-4 py-2  rounded-lg bg-blue-500 text-white shadow hover:bg-blue-600"
                          >
                            Mark Available
                          </button>
                        ) : (
                          <button
                            onClick={() => handleDelete(booking._id)}
                            className="p-2 rounded-full bg-red-500 text-white hover:bg-red-600"
                          >
                            <MdDelete size={22} />
                          </button>
                        )}
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </div>

            {/* Card layout for mobile */}
            {/* Card layout for tablet & small screens */}
            <div className="md:hidden divide-y">
              {data?.map((booking) => (
                <div
                  key={booking._id}
                  className="p-4 grid grid-cols-2 gap-y-2 gap-x-4 items-center"
                >
                  {/* Row 1 */}
                  <div className="font-semibold">Car Make</div>
                  <div>{booking.make}</div>

                  <div className="font-semibold">Reg Number</div>
                  <div>{booking.regNumber}</div>

                  {/* Row 2 */}
                  <div className="font-semibold">Start Date</div>
                  <div>{dayjs(booking.startDate).format("DD/MM/YYYY")}</div>

                  <div className="font-semibold">End Date</div>
                  <div>{dayjs(booking.endDate).format("DD/MM/YYYY")}</div>

                  {/* Row 3 */}
                  <div className="font-semibold">Amount</div>
                  <div>£{booking.totalPrice}</div>

                  <div className="font-semibold">Status</div>
                  <div>
                    <span
                      className={`px-2 py-1 rounded-md text-sm font-semibold ${
                        bookingStatus(booking.endDate).includes("Ended")
                          ? "bg-red-200 text-red-800"
                          : bookingStatus(booking.endDate).includes("today")
                          ? "bg-yellow-200 text-yellow-800"
                          : "bg-yellow-200 text-yellow-800"
                      }`}
                    >
                      {bookingStatus(booking.endDate)}
                    </span>
                  </div>

                  {/* Row 4 (Action full width under Status) */}
                  <div className="col-span-2 pt-2">
                    {!booking.isAvailable ? (
                      <button
                        onClick={() => handleAvailable(booking._id)}
                        className="w-full px-4 py-2 rounded-lg bg-blue-500 text-white shadow hover:bg-blue-600"
                      >
                        Mark Available
                      </button>
                    ) : (
                      <button
                        onClick={() => handleDelete(booking._id)}
                        className="w-full px-4 py-2 rounded-lg bg-red-500 text-white hover:bg-red-600"
                      >
                        Delete
                      </button>
                    )}
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

export default AllBookings;
