import dayjs from "dayjs";
import customParseFormat from "dayjs/plugin/customParseFormat.js";

export const dayDifference = (from, to) => {
  dayjs.extend(customParseFormat);
  // const d1 = new Date(from);
  // const d2 = new Date(to);
  // const timeDiff = Math.abs(d2 - d1);
  // const daysDiff = Math.ceil(timeDiff / (1000 * 60 * 60 * 24));
  const date1 = dayjs(from);
  const date2 = dayjs(to);

  const timeDiff = date2.diff(date1);
  const daysDiff = Math.ceil(timeDiff / (1000 * 60 * 60 * 24));

  return daysDiff;
};



export const bookingStatus = (endDate) => {
  const today = dayjs().startOf("day");
  const end = dayjs(endDate).startOf("day"); // works with "2025-09-14"

  if (today.isAfter(end)) {
    return `Booking Ended on ${end.format("DD/MM/YYYY")}`;
  } else if (today.isSame(end)) {
    return "Ends today";
  } else {
    const daysLeft = end.diff(today, "day");
    return `${daysLeft} day${daysLeft > 1 ? "s" : ""} left`;
  }
};
