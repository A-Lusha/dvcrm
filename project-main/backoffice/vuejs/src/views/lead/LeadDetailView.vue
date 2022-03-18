<script setup>
import { axios } from '@/common/api.service.js'
import { formatDate } from '@/common/datetimeFormat.js'

import { TrashIcon } from '@heroicons/vue/outline'
import { ChevronDownIcon } from '@heroicons/vue/solid'
import { Menu, MenuButton, MenuItem, MenuItems } from '@headlessui/vue'

import { onMounted, reactive } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const lead = reactive({})
const notes = reactive({ results: [] })
const leadOptions = reactive([
  { name: 'Contact', field: 'status', value: 'contacted' },
  { name: 'Scheduled Demo', field: 'status', value: 'demostart' },
])

async function loadLead() {
  axios
    .get(`/api/v1/leads/${route.params.id}/`)
    .then((response) => {
      Object.assign(lead, response.data)
    })
    .catch((error) => {
      console.log(error)
    })
}
async function editLead({ leadID, field, value }) {
  // TODO: possibly export this and others if reused in other places
  await axios
    .patch(`/api/v1/leads/${leadID}/`, { [field]: value })
    .then((response) => {
      console.log(response)
      loadLead()
      loadNotes()
    })
    .catch((error) => {
      console.log(error.response)
    })
}

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

onMounted(async () => {
  loadLead()
  loadNotes()
})
</script>

<template>
  <div class="md:grid md:grid-cols-4">
    <!-- Detail -->
    <section class="md:col-span-2 sm:m-5">
      <div class="bg-white shadow sm:rounded-lg">
        <div class="px-4 py-5 sm:px-6 flex justify-between items-center">
          <h2 class="text-xl leading-6 font-medium text-gray-900">Lead</h2>
          <span class="relative z-0 inline-flex shadow-sm rounded-md">
            <button
              type="button"
              class="relative inline-flex items-center px-4 py-2 rounded-l-md border border-gray-300 bg-white text-sm font-medium text-gray-700 hover:bg-gray-50 focus:z-10 focus:outline-none focus:ring-1 focus:ring-indigo-500 focus:border-indigo-500"
            >
              Edit Details
            </button>
            <Menu as="span" class="-ml-px relative block">
              <MenuButton
                class="relative inline-flex items-center px-2 py-2 rounded-r-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 focus:z-10 focus:outline-none focus:ring-1 focus:ring-indigo-500 focus:border-indigo-500"
              >
                <span class="sr-only">Open options</span>
                <ChevronDownIcon class="h-5 w-5" aria-hidden="true" />
              </MenuButton>
              <transition
                enter-active-class="transition ease-out duration-100"
                enter-from-class="transform opacity-0 scale-95"
                enter-to-class="transform opacity-100 scale-100"
                leave-active-class="transition ease-in duration-75"
                leave-from-class="transform opacity-100 scale-100"
                leave-to-class="transform opacity-0 scale-95"
              >
                <MenuItems
                  class="origin-top-right absolute right-0 mt-2 -mr-1 w-56 rounded-md shadow-lg bg-white ring-1 ring-black ring-opacity-5 focus:outline-none"
                >
                  <div class="py-1">
                    <MenuItem v-for="item in leadOptions" :key="item.value" v-slot="{ active }">
                      <a
                        @click.prevent="
                          editLead({ leadID: lead.id, field: item.field, value: item.value })
                        "
                        :class="[
                          active ? 'bg-gray-100 text-gray-900' : 'text-gray-700',
                          'block px-4 py-2 text-sm',
                        ]"
                      >
                        {{ item.name }}
                      </a>
                    </MenuItem>
                  </div>
                </MenuItems>
              </transition>
            </Menu>
          </span>
        </div>
        <div class="border-t border-gray-200 px-4 py-5 sm:px-6">
          <dl class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-1 gap-x-4 gap-y-8 xl:grid-cols-2">
            <div class="sm:col-span-1">
              <dt class="text-sm font-medium text-gray-500">Company name</dt>
              <dd class="mt-1 text-sm text-gray-900">{{ lead.company_name }}</dd>
            </div>
            <div class="sm:col-span-1">
              <dt class="text-sm font-medium text-gray-500">Status</dt>
              <dd class="mt-1 text-sm text-gray-900">{{ lead.status_display }}</dd>
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
                  <button
                    @click.prevent="removeNote(note.id)"
                    type="button"
                    class="inline-flex items-center p-1 border border-red-300 shadow-sm rounded bg-white hover:bg-red-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
                  >
                    <TrashIcon
                      class="flex-shrink-0 h-3 w-3 text-red-400 text-xs group-hover:text-red-700"
                    />
                  </button>
                  <span class="px-2 py-0.5 rounded bg-gray-100 text-gray-700 not-italic">{{
                    formatDate(note.created_at)
                  }}</span>
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
