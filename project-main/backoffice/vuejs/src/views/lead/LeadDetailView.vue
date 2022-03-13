<script setup>
import { axios } from '@/common/api.service.js'
import { formatDate } from '@/common/datetimeFormat.js'
import { onMounted, reactive } from 'vue'
import { useRoute } from 'vue-router'
import { TrashIcon } from '@heroicons/vue/outline'

const route = useRoute()
const lead = reactive({})
const notes = reactive({ results: [] })

async function loadNotes() {
  axios
    .get(`/api/v1/notes/?lead=${route.params.id}`)
    .then(response => {
      Object.assign(notes, response.data)
    })
    .catch(error => {
      console.log(error)
    })
}
async function addNote(e) {
  // TODO: better feedback
  const data = new FormData(e.target)
  data.append('lead', route.params.id)

  await axios
    .post('/api/v1/notes/', data)
    .then((response) => {
      e.target.reset()
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
    .then(response => response)
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

onMounted(() => {
  // Retrieve lead data
  axios
    .get(`/api/v1/leads/${route.params.id}/`)
    .then((response) => {
      Object.assign(lead, response.data)
    })
    .catch((error) => {
      console.log(error)
    })
  loadNotes()
})
</script>

<template>
  <div class="md:grid md:grid-cols-4">
    <!-- Detail -->
    <section class="md:col-span-2 sm:m-5">
      <div class="bg-white shadow sm:rounded-lg">
        <div class="px-4 py-5 sm:px-6">
          <h2 class="text-xl leading-6 font-medium text-gray-900">Lead Detail</h2>
        </div>
        <div class="border-t border-gray-200 px-4 py-5 sm:px-6">
          <dl class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-1 gap-x-4 gap-y-8 xl:grid-cols-2">
            <div class="sm:col-span-1">
              <dt class="text-sm font-medium text-gray-500">Company name</dt>
              <dd class="mt-1 text-sm text-gray-900">{{ lead.company_name }}</dd>
            </div>
            <div class="sm:col-span-1">
              <dt class="text-sm font-medium text-gray-500">Contact</dt>
              <dd class="mt-1 text-sm text-gray-900">
                {{ lead.contact_first_name }} {{ lead.contact_last_name }}
              </dd>
            </div>
            <div class="sm:col-span-1">
              <dt class="text-sm font-medium text-gray-500">Location</dt>
              <dd class="mt-1 text-sm text-gray-900">
                {{ lead.street }} <br />
                {{ lead.city }} {{ lead.state }} {{ lead.zipcode }}
              </dd>
            </div>
            <div class="sm:col-span-1">
              <dt class="text-sm font-medium text-gray-500">Phone</dt>
              <dd class="mt-1 text-sm text-gray-900">
                {{ lead.contact_phone }} {{ lead.contact_ext }}
              </dd>
            </div>
            <div class="sm:col-span-1">
              <dt class="text-sm font-medium text-gray-500">Email</dt>
              <dd class="mt-1 text-sm text-gray-900">{{ lead.contact_email }}</dd>
            </div>
            <div class="sm:col-span-1" v-if="lead.website">
              <dt class="text-sm font-medium text-gray-500">Website</dt>
              <dd class="mt-1 text-sm text-gray-900">{{ lead.website }}</dd>
            </div>
          </dl>
        </div>
      </div>
    </section>
    <!-- Notes -->
    <section class="md:col-span-2 mt-5 sm:m-5">
      <div class="bg-white shadow sm:rounded-lg divide-y">
        <div class="p-5">
          <h2 class="text-xl leading-6 font-medium text-gray-900">Lead Notes</h2>
        </div>
        <div v-if="notes.results.length">
          <ul role="list" class="divide-y">
            <li v-for="note in notes.results" :key="note.id" class="px-5 py-3 space-y-3">
              <div class="flex justify-between">
                <p class="font-bold text-sm text-indigo-800">{{ note.created_by.first_name }} {{ note.created_by.last_name }}</p>
                <p class="inline-flex items-center px-2 py-0.5 rounded text-xs bg-gray-100 text-gray-700 mt-1">{{ formatDate(note.created_at) }}</p>
              </div>
              <div class="text-sm text-gray-800">
                <p>{{ note.body }}</p>
              </div>
              <div class="flex justify-end">
                <!-- TODO: Add confirmation modal -->
                <button @click.prevent="removeNote(note.id)" type="button" class="inline-flex items-center p-1 border border-red-300 shadow-sm rounded bg-white hover:bg-red-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500">
                  <TrashIcon class="flex-shrink-0 h-3 w-3 text-red-400 text-xs group-hover:text-red-700"/>
                </button>
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
                <!-- Matches height of button in toolbar (1px border + 36px content height) -->
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
    </section>
  </div>
</template>

