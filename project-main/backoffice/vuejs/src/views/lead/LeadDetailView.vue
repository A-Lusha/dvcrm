<script setup>
import { axios } from '@/common/api.service.js'
import { ChevronDownIcon } from '@heroicons/vue/solid'
import { Menu, MenuButton, MenuItem, MenuItems } from '@headlessui/vue'
import NoteList from '@/components/NoteList.vue'
import { onMounted, reactive, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'

// TODO: field edits
// TODO: note pagination
// TODO: handle invalid lead instead of empty

// TODO: correct template input labels

const route = useRoute()
const router = useRouter()

let editingLead = ref(false)
const lead = reactive({})
const leadOptions = reactive([
  { name: 'Contact', field: 'status', value: 'contacted' },
  { name: 'Scheduled Demo', field: 'status', value: 'demostart' },
])
const noteList = ref(null)

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
async function editLead(leadID, payload) {
  // TODO: possibly export this
  // TODO: better feedback
  await axios
    .patch(`/api/v1/leads/${leadID}/`, payload)
    .then((response) => {
      console.log(response)
    })
    .catch((error) => {
      console.log(error)
    })
}
async function editDetails(editedLead) {
  // submit changes
  await editLead(editedLead.id, editedLead)
  // reset details page
  editingLead.value = false
  loadLead()
  noteList.value.loadNotes()
}

onMounted(loadLead)
</script>

<template>
  <div class="md:grid md:grid-cols-4">
    <!-- Detail -->
    <section class="md:col-span-2 sm:m-5">
      <div class="bg-white shadow sm:rounded-lg">
        <div class="px-4 py-5 flex justify-between items-center">
          <h2 class="text-xl leading-6 font-medium text-gray-900">Lead</h2>
          <span class="relative z-0 inline-flex shadow-sm rounded-md">
            <button
              type="button"
              @click="editingLead = true"
              v-show="!editingLead"
              class="relative inline-flex items-center px-4 py-2 rounded-l-md border border-gray-300 bg-white text-sm font-medium text-gray-700 hover:bg-gray-50 focus:z-10 focus:outline-none focus:ring-1 focus:ring-indigo-500 focus:border-indigo-500"
            >
              Edit Details
            </button>
            <button
              type="button"
              @click="editingLead = false"
              v-show="editingLead"
              class="relative inline-flex items-center px-4 py-2 rounded-l-md border border-gray-300 bg-red-200 text-sm font-medium text-gray-700 hover:bg-red-100 focus:z-10 focus:outline-none focus:ring-1 focus:ring-indigo-500 focus:border-indigo-500"
            >
              Cancel
            </button>
            <button
              type="button"
              @click="editDetails(lead)"
              v-show="editingLead"
              class="relative inline-flex items-center px-4 py-2 -ml-px border border-gray-300 bg-green-200 text-sm font-medium text-gray-700 hover:bg-green-100 focus:z-10 focus:outline-none focus:ring-1 focus:ring-indigo-500 focus:border-indigo-500"
            >
              Save Changes
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
                        @click.prevent="editLead(lead.id, { [item.field]: item.value })"
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
          <dl 
            @keyup.enter="editDetails(lead)"
            class="grid grid-cols-1 gap-x-4 gap-y-8 xl:grid-cols-2">
            <!-- Company Name -->
            <div class="sm:col-span-1">
              <dt class="font-medium text-gray-500 pt-1">
                <label for="company_name" class="block text-sm font-medium text-gray-700">
                  Company name
                </label>
              </dt>
              <dd>
                <p v-if="!editingLead" class="px-3 py-2">
                  {{ lead.company_name }}
                </p>
                <div
                  v-if="editingLead"
                  class="border-b border-gray-300 focus-within:border-indigo-600"
                >
                  <input
                    v-model="lead.company_name"
                    id="company_name"
                    type="text"
                    class="block w-full border-0 border-b border-transparent bg-gray-50 focus:border-indigo-600 focus:ring-0"
                  />
                </div>
              </dd>
            </div>
            <!-- Contact Name -->
            <div class="sm:col-span-1">
              <dt class="font-medium text-gray-500 pt-1">
                <label for="company_name" class="block text-sm font-medium text-gray-700">
                  Contact name
                </label>
              </dt>
              <dd>
                <p v-if="!editingLead" class="px-3 py-2 flex items-center space-x-2 -mb-1">
                  <span class="block w-1/2">
                    {{ lead.contact_first_name }}
                  </span>
                  <span class="block w-1/2">
                    {{ lead.contact_last_name }}
                  </span>
                </p>
                <div v-if="editingLead" class="flex -space-x-px">
                  <!-- First Name -->
                  <div class="w-1/2 border-b border-gray-300 focus-within:border-indigo-600">
                    <input
                      v-model="lead.contact_first_name"
                      id="company_name"
                      type="text"
                      class="block w-full border-0 border-b border-transparent bg-gray-50 focus:border-indigo-600 focus:ring-0 sm:text-sm"
                    />
                  </div>
                  <!-- Last Name -->
                  <div class="w-1/2 border-b border-gray-300 focus-within:border-indigo-600">
                    <input
                      v-model="lead.contact_last_name"
                      id="company_name"
                      type="text"
                      class="block w-full border-0 border-b border-transparent bg-gray-50 focus:border-indigo-600 focus:ring-0 sm:text-sm"
                    />
                  </div>
                </div>
              </dd>
            </div>
            <!-- Company Location -->
            <div class="sm:col-span-1">
              <dt class="font-medium text-gray-500 pt-1">
                <label for="location" class="block text-sm font-medium text-gray-700">
                  Location
                </label>
              </dt>
              <dd>
                <p v-if="!editingLead" class="px-3 py-2 -mb-1">
                  <div>{{ lead.street }}</div>
                  <div> {{ lead.city }} {{ lead.state }} {{ lead.zipcode }} </div>
                </p>
                <div v-if="editingLead" class="">
                  <div class="mt-1 bg-white rounded-md shadow-sm -space-y-px">
                    <div class="border-b border-gray-300 focus-within:border-indigo-600 mb-3">
                      <input
                        v-model="lead.street"
                        id="company_name"
                        type="text"
                        class="block w-full border-0 border-b border-transparent bg-gray-50 focus:border-indigo-600 focus:ring-0"
                      />
                    </div>
                    <div class="flex -space-x-px">
                      <!-- City -->
                      <div class="w-1/2 border-b border-gray-300 focus-within:border-indigo-600">
                        <input
                          v-model="lead.city"
                          id="company_name"
                          type="text"
                          class="block w-full border-0 border-b border-transparent bg-gray-50 focus:border-indigo-600 focus:ring-0 sm:text-sm"
                        />
                      </div>
                      <!-- State-->
                      <div class="w-1/4 border-b border-gray-300 focus-within:border-indigo-600">
                        <input
                          v-model="lead.state"
                          id="company_name"
                          type="text"
                          class="block w-full border-0 border-b border-transparent bg-gray-50 focus:border-indigo-600 focus:ring-0 sm:text-sm"
                        />
                      </div>
                      <!-- Zip Code -->
                      <div class="w-1/4 border-b border-gray-300 focus-within:border-indigo-600">
                        <input
                          v-model="lead.zipcode"
                          id="company_name"
                          type="text"
                          class="block w-full border-0 border-b border-transparent bg-gray-50 focus:border-indigo-600 focus:ring-0 sm:text-sm"
                        />
                      </div>
                    </div>
                  </div>
                </div>
              </dd>
            </div>
            <!-- Contact Phone -->
            <div class="sm:col-span-1">
              <dt class="font-medium text-gray-500 pt-1">
                <label for="company_name" class="block text-sm font-medium text-gray-700">
                  Contact Phone
                </label>
              </dt>
              <dd>
                <p v-if="!editingLead" class="px-3 py-2 flex items-center space-x-2 -mb-1">
                  <span class="block w-3/4">
                    {{ lead.contact_phone }}
                  </span>
                  <span v-if="lead.contact_ext" class="block w-1/4">
                    ext. {{ lead.contact_ext }}
                  </span>
                </p>
                <div v-if="editingLead" class="flex -space-x-px">
                  <!-- Phone -->
                  <div class="w-3/4 border-b border-gray-300 focus-within:border-indigo-600">
                    <input
                      v-model="lead.contact_phone"
                      id="company_name"
                      type="text"
                      class="block w-full border-0 border-b border-transparent bg-gray-50 focus:border-indigo-600 focus:ring-0 sm:text-sm"
                    />
                  </div>
                  <!-- Ext -->
                  <div class="w-1/4 border-b border-gray-300 focus-within:border-indigo-600">
                    <input
                      v-model="lead.contact_ext"
                      id="company_name"
                      type="text"
                      class="block w-full border-0 border-b border-transparent bg-gray-50 focus:border-indigo-600 focus:ring-0 sm:text-sm"
                    />
                  </div>
                </div>
              </dd>
            </div>
            <!-- Contact Email -->
            <div class="sm:col-span-1">
              <dt class="font-medium text-gray-500 pt-1">
                <label for="company_name" class="block text-sm font-medium text-gray-700">
                  Contact email
                </label>
              </dt>
              <dd>
                <p v-if="!editingLead" class="px-3 py-2">
                  {{ lead.contact_email }}
                </p>
                <div
                  v-if="editingLead"
                  class="border-b border-gray-300 focus-within:border-indigo-600"
                >
                  <input
                    v-model="lead.contact_email"
                    id="company_name"
                    type="text"
                    class="block w-full border-0 border-b border-transparent bg-gray-50 focus:border-indigo-600 focus:ring-0"
                  />
                </div>
              </dd>
            </div>
            <!-- Company Website -->
            <div class="sm:col-span-1">
              <dt class="font-medium text-gray-500 pt-1">
                <label for="company_name" class="block text-sm font-medium text-gray-700">
                  Website
                </label>
              </dt>
              <dd>
                <p v-if="!editingLead" class="px-3 py-2">
                  {{ lead.website }}
                </p>
                <div
                  v-if="editingLead"
                  class="border-b border-gray-300 focus-within:border-indigo-600"
                >
                  <input
                    v-model="lead.website"
                    id="company_name"
                    type="text"
                    class="block w-full border-0 border-b border-transparent bg-gray-50 focus:border-indigo-600 focus:ring-0"
                  />
                </div>
              </dd>
            </div>
          </dl>
        </div>
      </div>
    </section>
    <!-- Notes -->
    <section class="md:col-span-2 mt-5 sm:m-5">
      <NoteList ref="noteList" />
    </section>
  </div>
</template>
