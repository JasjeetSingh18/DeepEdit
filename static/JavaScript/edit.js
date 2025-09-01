function downloadPhoto(fileName) {
  const link = document.createElement("a");
  link.href = photo.src;
  link.download = fileName || "edited-photo.png";
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  updateStatus("Photo downloaded!");
}

const photo = document.getElementById("photo");
const cropArea = document.getElementById("cropArea");
const cropOverlay = document.getElementById("cropOverlay");
const photoContainer = document.getElementById("photo-container");
const statusDiv = document.getElementById("status");
const normalButtons = document.getElementById("normalButtons");
const cropButtons = document.getElementById("cropButtons");

let startX,
  startY,
  isDragging = false;
let cropSelection = null;
let cropMode = false;
let originalImageSrc = "";

function updateStatus(message) {
  if (statusDiv) {
    statusDiv.textContent = message;
    setTimeout(() => (statusDiv.textContent = ""), 3000);
  } else {
    console.log(message);
  }
}

function startCropMode() {
  cropMode = true;
  originalImageSrc = photo.src; // Store original image
  photo.classList.add("crop-mode");
  cropOverlay.style.display = "block";
  normalButtons.classList.add("hidden");
  cropButtons.classList.remove("hidden");
  cropButtons.classList.add("show-flex");
  updateStatus("Crop mode activated. Click and drag to select area to crop.");
}

function cancelCrop() {
  cropMode = false;
  photo.classList.remove("crop-mode");
  cropArea.style.display = "none";
  cropOverlay.style.display = "none";
  cropSelection = null;
  normalButtons.classList.remove("hidden");
  cropButtons.classList.add("hidden");
  cropButtons.classList.remove("show-flex");
  updateStatus("Crop cancelled.");
}

function finishCrop() {
  if (!cropSelection) {
    updateStatus("Please select an area to crop first!");
    return;
  }

  updateStatus("Applying crop...");

  const photoRect = photo.getBoundingClientRect();

  // Calculate scale factors
  const scaleX = photo.naturalWidth / photoRect.width;
  const scaleY = photo.naturalHeight / photoRect.height;

  // Calculate crop coordinates in original image dimensions
  const sx = cropSelection.left * scaleX;
  const sy = cropSelection.top * scaleY;
  const sw = cropSelection.width * scaleX;
  const sh = cropSelection.height * scaleY;

  // Validate crop dimensions
  if (sw <= 0 || sh <= 0) {
    updateStatus("Invalid crop dimensions!");
    return;
  }

  // Create canvas for cropping
  const canvas = document.createElement("canvas");
  canvas.width = sw;
  canvas.height = sh;
  const ctx = canvas.getContext("2d");

  try {
    ctx.drawImage(photo, sx, sy, sw, sh, 0, 0, sw, sh);
    const croppedDataURL = canvas.toDataURL("image/png");

    // Update the image
    photo.src = croppedDataURL;

    // Exit crop mode
    cropMode = false;
    photo.classList.remove("crop-mode");
    cropArea.style.display = "none";
    cropOverlay.style.display = "none";
    cropSelection = null;
    normalButtons.classList.remove("hidden");
    cropButtons.classList.add("hidden");
    cropButtons.classList.remove("show-flex");

    updateStatus("Photo cropped successfully!");
  } catch (error) {
    console.error("Crop error:", error);
    updateStatus("Error cropping image. Please try again.");
  }
}

photo.addEventListener("mousedown", (e) => {
  if (!cropMode) return; // Only allow dragging in crop mode

  e.preventDefault();
  isDragging = true;

  // Get coordinates relative to the photo container
  const containerRect = photoContainer.getBoundingClientRect();
  startX = e.clientX - containerRect.left;
  startY = e.clientY - containerRect.top;

  // Reset crop area
  cropArea.style.left = `${startX}px`;
  cropArea.style.top = `${startY}px`;
  cropArea.style.width = "0px";
  cropArea.style.height = "0px";
  cropArea.style.display = "block";

  updateStatus("Selecting crop area...");
});

document.addEventListener("mousemove", (e) => {
  if (!isDragging || !cropMode) return;

  const containerRect = photoContainer.getBoundingClientRect();
  const currentX = e.clientX - containerRect.left;
  const currentY = e.clientY - containerRect.top;

  // Calculate dimensions (handle negative values for backwards dragging)
  const width = Math.abs(currentX - startX);
  const height = Math.abs(currentY - startY);
  const left = Math.min(startX, currentX);
  const top = Math.min(startY, currentY);

  cropArea.style.left = `${left}px`;
  cropArea.style.top = `${top}px`;
  cropArea.style.width = `${width}px`;
  cropArea.style.height = `${height}px`;
});

document.addEventListener("mouseup", () => {
  if (isDragging && cropMode) {
    isDragging = false;

    // Store crop selection data
    const rect = cropArea.getBoundingClientRect();
    const photoRect = photo.getBoundingClientRect();

    if (rect.width > 10 && rect.height > 10) {
      // Minimum selection size
      cropSelection = {
        left: rect.left - photoRect.left,
        top: rect.top - photoRect.top,
        width: rect.width,
        height: rect.height,
      };
      updateStatus(
        `Crop area selected: ${Math.round(rect.width)}x${Math.round(
          rect.height
        )}px. Click "Finish Crop" to apply.`
      );
    } else {
      cropArea.style.display = "none";
      cropSelection = null;
      updateStatus("Selection too small. Try again.");
    }
  }
});

// Initialize - wait for image to load
photo.addEventListener("load", () => {
  updateStatus("Photo loaded. Ready for editing.");
});

// Handle case where image is already loaded
if (photo.complete && photo.naturalWidth > 0) {
  updateStatus("Photo ready for editing.");
}

function RevertImage() {
  photo.src = originalImageUrl;
  updateStatus("Reverted to original image.");
}

function adjustBrightness() {
  normalButtons.classList.add("hidden");
  brightnessButtons.classList.remove("hidden");
  originalImageSrc = photo.src;

  if (brightness !== null) {
    photo.style.filter = `brightness(${brightness}%)`;
    updateStatus(`Brightness adjusted to ${brightness}%.`);
  }
}

function updateBrightness(value) {
  brightness = value;
  photo.style.filter = `brightness(${brightness}%)`;
}

function applyBrightness() {
  const canvas = document.createElement("canvas");
  const ctx = canvas.getContext("2d");

  canvas.width = photo.naturalWidth;
  canvas.height = photo.naturalHeight;

  ctx.filter = `brightness(${brightness}%)`;

  ctx.drawImage(photo, 0, 0);

  photo.src = canvas.toDataURL("image/png");

  photo.style.filter = "";

  normalButtons.classList.remove("hidden");
  brightnessButtons.classList.add("hidden");

  updateStatus(`Brightness applied: ${brightness}%.`);
}

function cancelBrightness() {
  brightness = 100;
  photo.style.filter = `brightness(${brightness}%)`;
  normalButtons.classList.remove("hidden");
  brightnessButtons.classList.add("hidden");
  updateStatus("Brightness adjustment canceled.");
}

function applyFilter() {
  originalImageSrc = photo.src;
  normalButtons.classList.add("hidden");
  filterOptions.classList.remove("hidden");
}

function applyPilgramFilter(filterName) {
  updateStatus("Applying filter...");

  fetch("/apply_filter", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      filter_name: filterName,
      file_name: fileName, // Your current file name
    }),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        // Update the image source with the filtered version
        photo.src = baseUploadsUrl + data.filtered_image;
        updateStatus(`${filterName} filter applied successfully!`);
      } else {
        updateStatus(`Error: ${data.error}`);
      }
    })
    .catch((error) => {
      console.error("Error:", error);
      updateStatus("Error applying filter");
    });
}

function previewFilter(filterName) {
  // For real-time preview when hovering over filter options
  fetch("/preview_filter", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      filter_name: filterName,
      file_name: fileName,
    }),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        photo.src = baseUploadsUrl + data.preview_image;
      }
    });
}

function cancelFilter() {
  photo.src = originalImageSrc;
  document.getElementById("filterOptions").classList.add("hidden");
  normalButtons.classList.remove("hidden");

  const selectedFilter = document.querySelector('input[name="filter"]:checked');
  if (selectedFilter) {
    selectedFilter.checked = false;
  }

  updateStatus("Filter selection cancelled.");
}

function resetPreview() {
  photo.src = originalImageSrc;
}

function completeFilter() {
  document.getElementById("filterOptions").classList.add("hidden");
  normalButtons.classList.remove("hidden");
  updateStatus("Filter applied! Ready for more editing.");
}

function applySelectedFilter() {
  const selectedFilter = document.querySelector('input[name="filter"]:checked');
  if (selectedFilter) {
    applyPilgramFilter(selectedFilter.value);
    setTimeout(() => completeFilter(), 1000); // Auto-complete after applying
  } else {
    updateStatus("Please select a filter first!");
  }
}

function enhanceWithAI() {
  updateStatus("Enhancing image with AI...");
  fetch("/enhance_image", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      file_name: fileName,
    }),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        photo.src = baseUploadsUrl + data.enhanced_image;
        updateStatus("Image enhanced successfully!");
      } else {
        updateStatus(`Error: ${data.error}`);
      }
    })
    .catch((error) => {
      console.error("Error:", error);
      updateStatus("Error enhancing image");
    });
}
