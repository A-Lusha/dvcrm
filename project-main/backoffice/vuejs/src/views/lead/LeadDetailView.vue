<script setup>
import { axios } from '@/common/api.service.js'
import { onMounted, reactive } from 'vue'
import { useRoute } from 'vue-router'

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

  const data = new FormData(e.target)
  data.append('lead', route.params.id)

  await axios
    .post('/api/v1/notes/', data)
    .then(response => {
      e.target.reset()
      // TODO: better feedback
    })
    .catch(error => {
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
    .then(response => {
      Object.assign(lead, response.data)
    })
    .catch(error => {
      console.log(error)
    })
  loadNotes()
})
</script>

<template>
  <!-- Detail -->
  <section class="sm:m-5">
    <div class="bg-white shadow sm:rounded-lg">
      <div class="px-4 py-5 sm:px-6">
        <h2 class="text-lg leading-6 font-medium text-gray-900">Lead Information</h2>
      </div>
      <div class="border-t border-gray-200 px-4 py-5 sm:px-6">
        <dl class="grid grid-cols-1 gap-x-4 gap-y-8 sm:grid-cols-2">
          <div class="sm:col-span-1">
            <dt class="text-sm font-medium text-gray-500">Company name</dt>
            <dd class="mt-1 text-sm text-gray-900">{{ lead.company_name }}</dd>
          </div>
          <div class="sm:col-span-1">
            <dt class="text-sm font-medium text-gray-500">Contact</dt>
            <dd class="mt-1 text-sm text-gray-900">{{ lead.contact_first_name }} {{ lead.contact_last_name }}</dd>
          </div>
          <div class="sm:col-span-1">
            <dt class="text-sm font-medium text-gray-500">Location</dt>
            <dd class="mt-1 text-sm text-gray-900">
              {{ lead.street }} <br />
              {{ lead.city }} {{ lead.state }} {{ lead.zipcode}} 
            </dd>
          </div>
          <div class="sm:col-span-1">
            <dt class="text-sm font-medium text-gray-500">Phone</dt>
            <dd class="mt-1 text-sm text-gray-900">{{ lead.contact_phone }} {{ lead.contact_ext }}</dd>
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
  <section class="sm:m-5">
    <div class="bg-white shadow sm:rounded-lg sm:overflow-hidden">
      <div class="px-4 py-5 sm:px-6">
        <h2 class="text-lg font-medium text-gray-900">Notes</h2>
      </div>
      <div class="flex items-start space-x-4 px-5">
        <div class="min-w-0 flex-1">
          <form @submit.prevent="addNote" class="relative mb-5">
            <div class="border border-gray-300 rounded-lg shadow-sm overflow-hidden focus-within:border-indigo-500 focus-within:ring-1 focus-within:ring-indigo-500">
              <label for="comment" class="sr-only">Add a note</label>
              <textarea rows="2" name="body" id="body" class="block w-full py-3 border-0 resize-none focus:ring-0 sm:text-sm" placeholder="Add your comment..." />

              <!-- Spacer element to match the height of the toolbar -->
              <div class="py-2" aria-hidden="true">
                <!-- Matches height of button in toolbar (1px border + 36px content height) -->
                <div class="py-px">
                  <div class="h-9" />
                </div>
              </div>
            </div>

            <div class="absolute bottom-0 inset-x-0 pl-3 pr-2 py-2 flex justify-end">
              <div class="flex-shrink-0">
                <button type="submit" class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">Post</button>
              </div>
            </div>
          </form>
        </div>
      </div>
      
      <div class="divide-y divide-gray-200">
        <div v-if="notes.results.length" class="px-4 py-6 sm:px-6">
          <ul role="list" class="space-y-8">
            <li v-for="note in notes.results" :key="note.id" class="border-t pt-8">
              <div class="flex space-x-3">
                <div class="flex-shrink-0">
                  <img class="h-10 w-10 rounded-full" src="" alt="" />
                </div>
                <div>
                  <div class="text-sm font-medium text-gray-900">
                    <p>{{ note.created_by.first_name }} {{ note.created_by.last_name}}</p>
                  </div>
                  <div class="mt-1 text-sm text-gray-700">
                    <p>{{ note.body }}</p>
                  </div>
                  <div class="mt-2 text-sm space-x-2">
                    <span class="text-gray-500 font-medium">{{ note.created_at }}</span>
                  </div>
                </div>
              </div>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </section>
</template>
