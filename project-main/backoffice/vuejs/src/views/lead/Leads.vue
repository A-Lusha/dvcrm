<template>
  <div class="relative mx-4 lg:mx-8 pb-5 border-b border-gray-200 sm:pb-0">
    <div class="flex items-center justify-between my-5 lg:my-10 h-11 md:block">
      <h3 class="text-3xl lg:text-6xl inline font-medium text-gray-800">My Leads</h3>
      <div class="md:absolute md:top-8 lg:top-12 md:right-0">
        <button
          type="button"
          class="my-2 inline-flex py-2 px-3 items-center border border-transparent rounded-md shadow-sm font-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
        >
          New Lead <PlusCircleIcon class="ml-2 h-7 w-7" />
        </button>
      </div>
    </div>
    <div class="mt-6">
      <div class="sm:hidden">
        <label for="current-tab" class="sr-only">Select a tab</label>
        <select
          id="current-tab"
          name="current-tab"
          class="block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm rounded-md"
        >
          <option v-for="tab in tabs" :key="tab.name" :selected="tab.current">
            {{ tab.name }}
          </option>
        </select>
      </div>
      <div class="hidden sm:block">
        <nav class="-mb-px flex space-x-8">
          <a
            v-for="tab in tabs"
            :key="tab.name"
            :href="tab.href"
            :class="[
              tab.current
                ? 'border-indigo-500 text-indigo-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300',
              'whitespace-nowrap pb-4 px-1 border-b-2 font-medium text-sm',
            ]"
            :aria-current="tab.current ? 'page' : undefined"
          >
            {{ tab.name }}
          </a>
        </nav>
      </div>
    </div>
  </div>
  <AppLeadList :leads="leads" />
</template>

<script>
import { axios } from '@/common/api.service.js'
import { PlusCircleIcon } from '@heroicons/vue/solid'
import AppLeadList from '@/components/LeadList.vue'
import { onMounted, ref } from 'vue'

export default {
  components: {
    PlusCircleIcon,
    AppLeadList,
  },
  setup() {
    // TODO: query change
    const tabs = [
      { name: 'All', href: '#', current: false },
      { name: 'New', href: '#', current: false },
      { name: 'Contacted', href: '#', current: false },
      { name: 'Scheduled', href: '#', current: true },
      { name: 'Completed', href: '#', current: false },
      { name: 'Sent', href: '#', current: false },
      { name: 'Signed', href: '#', current: false },
    ]
    // TODO: make not dummy data
    let leads = ref([
      {
        id: 1,
        company: 'Johnson Inc.',
        contact_person: 'John Johnson',
        phone: '555-555-5555',
        email: 'test@test.com',
        created_at: '2020-01-07',
        assigned_to: 'Alex Nelson',
        status: 'New',
      },
      {
        id: 2,
        company: 'Johnson Inc.',
        contact_person: 'John Johnson',
        phone: '555-555-5555',
        email: 'test@test.com',
        created_at: '2020-01-07',
        assigned_to: 'Alex Nelson',
        status: 'New',
      },
      {
        id: 3,
        company: 'Johnson Inc.',
        contact_person: 'John Johnson',
        phone: '555-555-5555',
        email: 'test@test.com',
        created_at: '2020-01-07',
        assigned_to: 'Alex Nelson',
        status: 'New',
      },
    ])
    onMounted(async () => {
      leads.value = await axios.get('http://127.0.0.1:8000/api/v1/leads/').then(
        (r) => r.data.results,
        (e) => {
          console.log(e.message)
        }
      )
    })
    return {
      tabs,
      leads,
    }
  },
}
</script>
