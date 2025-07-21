<template>
  <div class="view-container">
    <h2 class="view-title">Documents</h2>
    <div class="view-card">
      <!-- Document upload UI here -->
      <div class="documents-upload">
        <h3>Upload Documents</h3>
        <div class="upload-area" @dragover.prevent @drop.prevent="handleDrop">
          <input type="file" multiple ref="fileInput" @change="handleFiles" style="display:none" />
          <div class="upload-instructions" @click="triggerFileInput">
            <span style="font-size:2rem;">📤</span>
            <p>Drag & drop files here or <span class="upload-link">browse</span> to upload</p>
          </div>
        </div>
        <div v-if="files.length" class="file-preview-list">
          <div v-for="(file, idx) in files" :key="idx" class="file-preview">
            <span style="font-size:1.2rem;">📄</span>
            <span>{{ file.name }}</span>
          </div>
          <button class="upload-btn" @click="uploadFiles">Upload</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const fileInput = ref(null);
const files = ref([]);

function triggerFileInput() {
  fileInput.value.click();
}

function handleFiles(e) {
  const selected = Array.from(e.target.files);
  files.value = [...files.value, ...selected];
}

function handleDrop(e) {
  const dropped = Array.from(e.dataTransfer.files);
  files.value = [...files.value, ...dropped];
}

function uploadFiles() {
  // Placeholder for upload logic
  alert('Files uploaded!');
  files.value = [];
}
</script>

<style>
.view-container {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
}
.view-title {
  color: #1e3c72;
  font-size: 2.2rem;
  font-weight: 700;
  margin-bottom: 32px;
}
.view-card {
  transition: box-shadow 0.2s, transform 0.2s;
  background: linear-gradient(120deg, #e3eafc 0%, #f8fbff 100%);
  box-shadow: 0 2px 12px rgba(30,60,114,0.08);
  border-radius: 16px;
  padding: 40px 32px;
  margin-bottom: 32px;
  color: #1e3c72;
}
.view-card:hover {
  box-shadow: 0 8px 32px rgba(30,60,114,0.18);
  transform: translateY(-2px) scale(1.03);
  background: linear-gradient(120deg, #2a5298 0%, #1e3c72 100%);
  color: #fff;
}
.documents-upload {
  max-width: 600px;
  margin: 0 auto;
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 2px 12px rgba(30,60,114,0.08);
  padding: 32px;
  color: #1e3c72;
}
.upload-area {
  border: 2px dashed #2a5298;
  border-radius: 12px;
  background: #e3eafc;
  padding: 32px;
  text-align: center;
  cursor: pointer;
  margin-bottom: 24px;
  transition: border-color 0.2s;
}
.upload-area:hover {
  border-color: #1e3c72;
}
.upload-instructions {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  color: #2a5298;
  font-size: 1.1rem;
}
.upload-link {
  color: #1e3c72;
  text-decoration: underline;
  cursor: pointer;
}
.file-preview-list {
  margin-top: 18px;
}
.file-preview {
  display: flex;
  align-items: center;
  gap: 12px;
  background: #e3eafc;
  border-radius: 8px;
  padding: 10px 18px;
  margin-bottom: 8px;
  color: #1e3c72;
}
.upload-btn {
  margin-top: 16px;
  background: linear-gradient(120deg, #1e3c72 0%, #2a5298 100%);
  color: #fff;
  border: none;
  border-radius: 8px;
  padding: 12px 32px;
  font-size: 1.08rem;
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(30,60,114,0.08);
  transition: background 0.2s;
}
.upload-btn:hover {
  background: linear-gradient(120deg, #2a5298 0%, #1e3c72 100%);
}
@media (max-width: 700px) {
  .documents-upload {
    padding: 12px;
  }
  .upload-area {
    padding: 12px;
  }
}
</style>
