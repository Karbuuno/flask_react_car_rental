import React from "react";

import { CheckCircle } from "lucide-react";

function SuccessPage() {
  return (
    <div className='flex items-center justify-center h-screen bg-gray-100'>
      <div className='bg-white shadow-xl rounded-2xl p-10 max-w-md text-center'>
        <CheckCircle className='w-16 h-16 text-green-500 mx-auto mb-4' />

        <h1 className='text-2xl font-bold text-gray-800 mb-2'>
          Payment Successful 🎉
        </h1>

        <p className='text-gray-600 mb-6'>
          Thank you for your booking! Your payment has been received and your
          car is reserved.
        </p>

        <a
          href='/'
          className='bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-6 rounded-lg shadow-md transition'
        >
          Go to Home
        </a>
      </div>
    </div>
  );
}

export default SuccessPage;
