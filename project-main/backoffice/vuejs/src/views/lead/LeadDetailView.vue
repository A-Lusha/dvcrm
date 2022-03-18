<script setup>
import { axios } from '@/common/api.service.js'
import { ChevronDownIcon } from '@heroicons/vue/solid'
import { Menu, MenuButton, MenuItem, MenuItems } from '@headlessui/vue'
import NoteList from '@/components/NoteList.vue'
import { onMounted, reactive, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()
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
async function editLead({ leadID, field, value }) {
  // TODO: possibly export this and others if reused in other places
  await axios
    .patch(`/api/v1/leads/${leadID}/`, { [field]: value })
    .then((response) => {
      console.log(response)
      loadLead()
      noteList.value.loadNotes()
    })
    .catch((error) => {
      console.log(error)
    })
}

onMounted(async () => {
  loadLead()
})
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
              @click="router.back"
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
      <NoteList ref="noteList" />
    </section>
  </div>
</template>
