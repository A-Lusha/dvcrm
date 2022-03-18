<script setup>
import { axios } from '@/common/api.service.js'
import { PlusSmIcon } from '@heroicons/vue/outline'
import AppLeadList from '@/components/LeadList.vue'
import { onMounted, ref, reactive } from 'vue'

const currentStatus = ref(0)
const leads = ref({ page: 1, pageSize: 8 })
const tabs = reactive([
  { name: 'All', query: '', current: true },
  { name: 'New', query: 'newlead', current: false },
  { name: 'Contacted', query: 'contacted', current: false },
  { name: 'Scheduled', query: 'demostart', current: false },
  { name: 'Completed', query: 'demodone', current: false },
  { name: 'Sent', query: 'appstart', current: false },
  { name: 'Signed', query: 'appdone', current: false },
  { name: 'Probation', query: 'probation', current: false },
])

async function changePage(page) {
  leads.value.page = leads.value.page + page
  getLeads()
}
async function changeFilter(index) {
  // Change which filter is visually active
  for (const [i, tab] of tabs.entries()) tab.current = i !== index ? false : true
  currentStatus.value = index
  leads.value.page = 1
  getLeads()
}
async function getLeads() {
  const url = `/api/v1/leads/?page=${leads.value.page}&status=${tabs[currentStatus.value].query}`
  await axios
    .get(url)
    .then(({ data }) => {
      Object.assign(leads.value, data)
    })
    .catch((e) => console.log(e.message))
}

onMounted(getLeads)
</script>

<template>
  <div class="relative mx-6 lg:mx-8 pb-5 border-b border-gray-200 md:pb-0">
    <div class="flex items-center justify-between my-5 lg:my-10 h-11 md:block">
      <h3 class="text-3xl lg:text-6xl inline font-medium text-gray-800">My Leads</h3>
      <div class="md:absolute md:top-8 lg:top-12 md:right-0">
        <RouterLink
          :to="{ name: 'AddLead' }"
          class="inline-flex items-center p-3 border border-transparent rounded-full shadow-lg text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
        >
          <PlusSmIcon class="h-6 w-6" aria-hidden="true" />
        </RouterLink>
      </div>
    </div>
    <div class="mt-6">
      <div class="md:hidden">
        <label for="current-tab" class="sr-only">Filter by status</label>
        <select
          v-model="currentStatus"
          @change="changeFilter(currentStatus)"
          id="current-tab"
          name="current-tab"
          class="block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm rounded-md"
        >
          <option v-for="(tab, index) in tabs" :key="index" :selected="tab.current" :value="index">
            {{ tab.name }}
          </option>
        </select>
      </div>
      <div class="hidden md:block">
        <nav class="-mb-px flex space-x-8">
          <button
            v-for="(tab, index) in tabs"
            :key="tab.name"
            :class="[
              tab.current
                ? 'border-indigo-500 text-indigo-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300',
              'whitespace-nowrap pb-4 px-1 border-b-2 font-medium text-sm',
            ]"
            :aria-current="tab.current ? 'page' : undefined"
            @click.prevent="changeFilter(index)"
          >
            {{ tab.name }}
          </button>
        </nav>
      </div>
    </div>
  </div>
  <AppLeadList :leads="leads.results" />
  <nav
    class="bg-inherit px-4 py-3 flex items-center mx-6 lg:mx-8 justify-between border-t border-gray-200 sm:px-6"
    aria-label="Pagination"
    v-if="leads.count > leads.pageSize"
  >
    <div class="hidden sm:block">
      <p class="text-sm text-gray-700">
        Showing
        <span class="font-medium">{{ (leads.page - 1) * leads.pageSize + 1 }}</span>
        to
        <span class="font-medium">{{
          (leads.page - 1) * leads.pageSize + leads.results.length
        }}</span>
        of
        <span class="font-medium">{{ leads.count }}</span>
        results
      </p>
    </div>
    <div class="flex-1 flex justify-between sm:justify-end">
      <button
        :disabled="!leads.previous"
        type="button"
        @click.prevent="changePage(-1)"
        class="disabled:opacity-80 relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
      >
        Previous
      </button>
      <button
        :disabled="!leads.next"
        type="button"
        @click.prevent="changePage(1)"
        class="disabled:opacity-80 ml-3 relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
      >
        Next
      </button>
    </div>
  </nav>
</template>
