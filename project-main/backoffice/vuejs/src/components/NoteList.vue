<script setup>
import { axios } from '@/common/api.service.js'
import { formatDate } from '@/common/datetimeFormat.js'
import { TrashIcon } from '@heroicons/vue/outline'
import { useRoute } from 'vue-router'
import { onMounted, reactive } from 'vue'

const notes = reactive({ results: [] })
const route = useRoute()

async function loadNotes() {
  axios
    .get(`/api/v1/notes/?lead=${route.params.id}`)
    .then((response) => {
      Object.assign(notes, response.data)
    })
    .catch((error) => {
      console.log(error)
    })
}
async function addNote({ target: form }) {
  // TODO: better feedback
  const data = new FormData(form)
  data.append('lead', route.params.id)

  await axios
    .post('/api/v1/notes/', data)
    .then((response) => {
      form.reset()
    })
    .catch((error) => {
      if (error.response) {
        for (const property in error.response.data) {
          console.log(`${property}: ${error.response.data[property]}`)
        }
      } else if (error.message) {
        console.log(error.message)
      }
    })
  loadNotes()
}
async function removeNote(noteID) {
  // TODO: better feedback
  await axios
    .delete(`/api/v1/notes/${noteID}`)
    .then((response) => response)
    .catch((error) => {
      if (error.response) {
        for (const property in error.response.data) {
          console.log(`${property}: ${error.response.data[property]}`)
        }
      } else if (error.message) {
        console.log(error.message)
      }
    })
  loadNotes()
}

defineExpose({ loadNotes })

onMounted(loadNotes())
</script>

<template>
  <div class="bg-white shadow sm:rounded-lg divide-y">
    <div class="p-5">
      <h2 class="text-xl leading-6 font-medium text-gray-900">Notes</h2>
    </div>
    <div v-if="notes.results.length">
      <ul role="list" class="divide-y">
        <li
          v-for="note in notes.results"
          :key="note.id"
          :class="[
            note.created_by ? 'bg-inherit' : 'bg-gray-200 border-l-2 italic border-l-red-500',
            'px-3 py-2 space-y-1 text-gray-800 text-sm',
          ]"
        >
          <div class="flex justify-between items-center">
            <p class="font-bold text-sm flex items-center">
              <span class="text-indigo-800" v-if="note.created_by">
                {{ note.created_by.first_name }} {{ note.created_by.last_name }}
              </span>
              <span class="text-red-800" v-else> System </span>
            </p>
            <p class="inline-flex items-center text-xs space-x-2">
              <span class="px-2 py-0.5 rounded bg-gray-100 text-gray-700 not-italic">{{
                formatDate(note.created_at)
              }}</span>
              <button
                @click.prevent="removeNote(note.id)"
                type="button"
                class="inline-flex items-center p-1 border border-red-300 shadow-sm rounded bg-white hover:bg-red-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
              >
                <TrashIcon
                  class="flex-shrink-0 h-3 w-3 text-red-400 text-xs group-hover:text-red-700"
                />
              </button>
            </p>
          </div>
          <div class="whitespace-pre-wrap">
            <p>{{ note.body }}</p>
          </div>
          <div class="flex justify-end">
            <!-- TODO: Add confirmation modal -->
          </div>
        </li>
      </ul>
    </div>
    <div class="p-5">
      <form @submit.prevent="addNote" class="relative">
        <div
          class="border border-gray-300 rounded-lg overflow-hidden focus-within:border-indigo-500 focus-within:ring-1 focus-within:ring-indigo-500"
        >
          <label for="comment" class="sr-only">Add a note</label>
          <textarea
            rows="2"
            name="body"
            id="body"
            class="block w-full py-3 border-0 resize-none focus:ring-0 sm:text-sm"
            placeholder="Add a new note..."
            required
          />
          <!-- Spacer element to match the height of the toolbar -->
          <div class="py-2 bg-white" aria-hidden="true">
            <div class="py-px">
              <div class="h-9" />
            </div>
          </div>
        </div>

        <div class="absolute bottom-0 right-0 p-2">
          <button
            type="submit"
            class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadhow-sm hover:shadow-none text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
          >
            Post
          </button>
        </div>
      </form>
    </div>
  </div>
</template>
