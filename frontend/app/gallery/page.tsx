"use client";

import React, { useEffect, useState } from "react";
import Image from "next/image";

interface GeneratedImage {
  id: string;
  prompt: string;
  cloudinary_url: string;
  created_at: string;
}

export default function GalleryPage() {
  const [images, setImages] = useState<GeneratedImage[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchGallery() {
      try {
        const res = await fetch("http://localhost:8000/api/v1/creative/gallery");
        if (!res.ok) throw new Error("Failed to fetch");
        const data = await res.json();
        setImages(data);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    }
    fetchGallery();
  }, []);

  if (loading) return <div className="p-8">Loading Gallery...</div>;

  return (
    <div className="p-8">
      <h1 className="text-3xl font-bold mb-6">Creative Studio Gallery</h1>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {images.map((img) => (
          <div key={img.id} className="border rounded-lg p-4 flex flex-col gap-2">
            {/* The prompt explicitly asks to render <img src="REAL_CLOUDINARY_URL" /> or equivalent */}
            <img 
              src={img.cloudinary_url} 
              alt={img.prompt} 
              className="w-full h-auto rounded object-cover aspect-square"
            />
            <p className="text-sm mt-2 text-gray-700">{img.prompt}</p>
          </div>
        ))}
        {images.length === 0 && <p>No images generated yet.</p>}
      </div>
    </div>
  );
}
