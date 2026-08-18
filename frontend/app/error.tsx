"use client";

import { useEffect } from "react";

export default function GlobalError({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  useEffect(() => {
    // Log the error to an error reporting service
    console.error(error);
  }, [error]);

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-50 text-gray-900">
      <div className="max-w-md w-full space-y-8 p-10 bg-white rounded-xl shadow-lg text-center">
        <h2 className="text-3xl font-bold text-red-600">Something went wrong!</h2>
        <p className="text-gray-600">
          We encountered an unexpected error. Please try again.
        </p>
        <button
          onClick={() => reset()}
          className="mt-4 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition"
        >
          Try again
        </button>
      </div>
    </div>
  );
}
