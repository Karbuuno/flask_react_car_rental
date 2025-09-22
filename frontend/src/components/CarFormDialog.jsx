import React, { useState, useEffect } from "react";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { useMutation, useQueryClient } from "react-query";
import { addCar, updateCar } from "@/components/api/api";
import { useNavigate } from "react-router-dom";

function CarFormDialog({ buttonTitle = "Add Car", carToEdit }) {
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const [formData, setFormData] = useState({
    name: "",
    carType: "",
    regNumber: "",
    seats: "",
    location: "",
    price: "",
    isAvailable: true,
  });
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState("");

  useEffect(() => {
    if (carToEdit) {
      setFormData({
        name: carToEdit.name || "",
        carType: carToEdit.carType || "",
        regNumber: carToEdit.regNumber || "",
        seats: carToEdit.seats || "",
        location: carToEdit.location || "",
        price: carToEdit.price || "",
        isAvailable: carToEdit.isAvailable,
      });
      // ✅ show existing image if editing
      if (carToEdit.image) {
        setPreview(carToEdit.image);
      }
    }
  }, [carToEdit]);

  const mutation = useMutation({
    mutationFn: (data) => {
      return carToEdit ? updateCar(carToEdit._id, data) : addCar(data);
    },
    onSuccess: () => {
      queryClient.invalidateQueries("cars");
    },
  });

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    setFile(selectedFile);
    if (selectedFile) {
      setPreview(URL.createObjectURL(selectedFile));
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const data = new FormData();
    Object.entries(formData).forEach(([key, value]) => {
      data.append(key, value);
    });
    if (file) {
      data.append("file", file);
    }
    mutation.mutate(data);

    setFormData({
      name: "",
      carType: "",
      regNumber: "",
      seats: "",
      location: "",
      price: "",
      isAvailable: true,
    });
    setFile(null);
    setPreview("");
    navigate("/cars/admin/dashboard");
  };

  return (
    <Dialog>
      <DialogTrigger asChild>
        <button className="px-4 py-2 rounded-lg bg-green-500 text-white hover:bg-green-600">
          {buttonTitle}
        </button>
      </DialogTrigger>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>{carToEdit ? "Edit Car" : "Add Car"}</DialogTitle>
        </DialogHeader>
        <form onSubmit={handleSubmit} className="space-y-4">
          <input
            type="text"
            placeholder="Car Name"
            value={formData.name}
            onChange={(e) => setFormData({ ...formData, name: e.target.value })}
            className="w-full border p-2 rounded"
            required
          />
          <input
            type="text"
            placeholder="Car Type"
            value={formData.carType}
            onChange={(e) =>
              setFormData({ ...formData, carType: e.target.value })
            }
            className="w-full border p-2 rounded"
            required
          />
          <input
            type="text"
            placeholder="Reg Number"
            value={formData.regNumber}
            onChange={(e) =>
              setFormData({ ...formData, regNumber: e.target.value })
            }
            className="w-full border p-2 rounded"
            required
          />
          <input
            type="number"
            placeholder="Seats"
            value={formData.seats}
            onChange={(e) =>
              setFormData({ ...formData, seats: e.target.value })
            }
            className="w-full border p-2 rounded"
            required
          />
          <input
            type="text"
            placeholder="Location"
            value={formData.location}
            onChange={(e) =>
              setFormData({ ...formData, location: e.target.value })
            }
            className="w-full border p-2 rounded"
            required
          />
          <input
            type="number"
            placeholder="Price"
            value={formData.price}
            onChange={(e) =>
              setFormData({ ...formData, price: +e.target.value })
            }
            className="w-full border p-2 rounded"
            required
          />

          {/* ✅ File Upload with Preview */}
          <input
            type="file"
            accept="image/*"
            onChange={handleFileChange}
            className="w-full border p-2 rounded"
          />
          {preview && (
            <img
              src={preview}
              alt="Preview"
              className="mt-4 w-48 h-32 object-cover rounded border"
            />
          )}

          <button
            type="submit"
            className="w-full py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
          >
            {carToEdit ? "Update Car" : "Add Car"}
          </button>
        </form>
      </DialogContent>
    </Dialog>
  );
}

export default CarFormDialog;
