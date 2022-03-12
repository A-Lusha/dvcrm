<template>
  <div class="bg-white shadow overflow-hidden sm:rounded-md">
    <ul role="list" class="divide-y divide-gray-200">
      <li v-for="lead in leads" :key="lead.id">
        <RouterLink :to="{ name: 'LeadDetail', params: { id: lead.id }}" class="block hover:bg-gray-50">
          <div class="px-4 py-4 sm:px-6">
            <div class="flex items-center justify-between">
              <p class="text-sm font-medium text-indigo-600 truncate">
                {{ lead.company_name }}
              </p>
              <div class="ml-2 flex-shrink-0 flex">
                <p
                  class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800"
                >
                  {{ lead.status }}
                </p>
              </div>
            </div>
            <div class="mt-2 sm:flex sm:justify-between">
              <div class="sm:flex">
                <p class="flex items-center text-sm text-gray-500">
                  <UsersIcon
                    class="flex-shrink-0 mr-1.5 h-5 w-5 text-gray-400"
                    aria-hidden="true"
                  />
                  {{ lead.contact_phone }}
                </p>
                <p class="mt-2 flex items-center text-sm text-gray-500 sm:mt-0 sm:ml-6">
                  <LocationMarkerIcon
                    class="flex-shrink-0 mr-1.5 h-5 w-5 text-gray-400"
                    aria-hidden="true"
                  />
                  {{ lead.assigned_to.first_name }} {{ lead.assigned_to.last_name }}
                </p>
              </div>
              <div class="mt-2 flex items-center text-sm text-gray-500 sm:mt-0">
                <CalendarIcon
                  class="flex-shrink-0 mr-1.5 h-5 w-5 text-gray-400"
                  aria-hidden="true"
                />
                <p>
                  {{ `Requested ` }}
                  <time :datetime="lead.created_at">{{
                    new Date(lead.created_at).toLocaleString()
                  }}</time>
                </p>
              </div>
            </div>
          </div>
        </RouterLink>
      </li>
    </ul>
  </div>
</template>

<script setup>
import { CalendarIcon, LocationMarkerIcon, UsersIcon } from '@heroicons/vue/solid'
const props = defineProps({
  leads: Array
})
</script>
