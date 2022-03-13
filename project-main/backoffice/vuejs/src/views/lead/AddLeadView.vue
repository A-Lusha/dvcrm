<script setup>
import { axios } from '@/common/api.service.js'
import { useRouter } from 'vue-router'

const router = useRouter()

function resetForm(form) {
  for (const [id] of form.entries()) {
    const field = document.getElementById(id)
    field.classList.add('field_no-errors')
    field.classList.remove('field_has-errors')
  }
  document.querySelectorAll('.error-msg').forEach(el => el.remove())
}

function displayErrors(fieldErrors) {
  for (const id in fieldErrors) {
    const field = document.getElementById(id)
    field.classList.remove('field_no-errors')
    field.classList.add('field_has-errors')

    const display = document.createElement('span')
    display.classList.add('text-red-700', 'text-sm', 'error-msg')
    display.innerText = fieldErrors[id]
    field.parentElement.appendChild(display)

    // TODO: remove
    console.log(`${id}: ${fieldErrors[id]}`)
  }
}

async function submitForm(e) {
  const formData = new FormData(e.target)
  resetForm(formData)

  await axios
    .post('/api/v1/leads/', formData)
    .then(response => {
      router.push({ name: 'Leads' })
    })
    .catch(error => {
      if(error.response.data) {
        displayErrors(error.response.data)
      } else {
        console.log(error)
      }
    })
}
</script>

<template>
  <form class="p-5" @submit.prevent="submitForm" id="form">
    <!-- Company Information -->
    <div class="mt-10 sm:mt-0">
      <div class="md:grid md:grid-cols-4 md:gap-6">
        <div class="md:col-span-1">
          <div class="px-4 sm:px-0">
            <h3 class="text-xl font-medium leading-6 text-gray-900">Company Information</h3>
          </div>
        </div>
        <div class="mt-5 md:mt-0 md:col-span-3">
          <div class="px-4 py-5 bg-white sm:p-6 shadow overflow-hidden sm:rounded-md">
            <div class="grid grid-cols-6 gap-6">
              <div class="col-span-6 sm:col-span-3">
                <label for="company_name" class="block text-sm font-medium text-gray-700">Company name</label>
                <input type="text" name="company_name" id="company_name" class="mt-1 field_no-errors block w-full shadow-sm sm:text-sm rounded-md" />
              </div>

              <div class="col-span-6 sm:col-span-3">
                <label for="website" class="block text-sm font-medium text-gray-700">Website</label>
                <div class="mt-1 flex rounded-md shadow-sm">
                  <span class="inline-flex items-center px-3 rounded-l-md border border-r-0 bg-gray-50 text-gray-500 text-sm"> http:// </span>
                  <input type="text" name="website" id="website" class="field_no-errors flex-1 block w-full rounded-none rounded-r-md sm:text-sm" placeholder="www.example.com" />
                </div>
              </div>

              <div class="col-span-6">
                <label for="street" class="block text-sm font-medium text-gray-700">Street address</label>
                <input type="text" name="street" id="street" class="mt-1 field_no-errors block w-full shadow-sm sm:text-sm rounded-md" />
              </div>

              <div class="col-span-6 lg:col-span-2">
                <label for="city" class="block text-sm font-medium text-gray-700">City</label>
                <input type="text" name="city" id="city" class="mt-1 field_no-errors block w-full shadow-sm sm:text-sm rounded-md" />
              </div>

              <div class="col-span-6 sm:col-span-3 lg:col-span-2">
                <label for="state" class="block text-sm font-medium text-gray-700">State</label>
                <select id="state" name="state" class="mt-1 block w-full py-2 px-3 border bg-white rounded-md shadow-sm focus:outline-none field_no-errors sm:text-sm">
                    <option value="" selected>Select a state</option>
                  	<option value="AL">Alabama</option>
                    <option value="AK">Alaska</option>
                    <option value="AZ">Arizona</option>
                    <option value="AR">Arkansas</option>
                    <option value="CA">California</option>
                    <option value="CO">Colorado</option>
                    <option value="CT">Connecticut</option>
                    <option value="DE">Delaware</option>
                    <option value="DC">District Of Columbia</option>
                    <option value="FL">Florida</option>
                    <option value="GA">Georgia</option>
                    <option value="HI">Hawaii</option>
                    <option value="ID">Idaho</option>
                    <option value="IL">Illinois</option>
                    <option value="IN">Indiana</option>
                    <option value="IA">Iowa</option>
                    <option value="KS">Kansas</option>
                    <option value="KY">Kentucky</option>
                    <option value="LA">Louisiana</option>
                    <option value="ME">Maine</option>
                    <option value="MD">Maryland</option>
                    <option value="MA">Massachusetts</option>
                    <option value="MI">Michigan</option>
                    <option value="MN">Minnesota</option>
                    <option value="MS">Mississippi</option>
                    <option value="MO">Missouri</option>
                    <option value="MT">Montana</option>
                    <option value="NE">Nebraska</option>
                    <option value="NV">Nevada</option>
                    <option value="NH">New Hampshire</option>
                    <option value="NJ">New Jersey</option>
                    <option value="NM">New Mexico</option>
                    <option value="NY">New York</option>
                    <option value="NC">North Carolina</option>
                    <option value="ND">North Dakota</option>
                    <option value="OH">Ohio</option>
                    <option value="OK">Oklahoma</option>
                    <option value="OR">Oregon</option>
                    <option value="PA">Pennsylvania</option>
                    <option value="RI">Rhode Island</option>
                    <option value="SC">South Carolina</option>
                    <option value="SD">South Dakota</option>
                    <option value="TN">Tennessee</option>
                    <option value="TX">Texas</option>
                    <option value="UT">Utah</option>
                    <option value="VT">Vermont</option>
                    <option value="VA">Virginia</option>
                    <option value="WA">Washington</option>
                    <option value="WV">West Virginia</option>
                    <option value="WI">Wisconsin</option>
                    <option value="WY">Wyoming</option>
                </select>
              </div>

              <div class="col-span-6 sm:col-span-3 lg:col-span-2">
                <label for="zipcode" class="block text-sm font-medium text-gray-700">ZIP / Postal code</label>
                <input type="text" name="zipcode" id="zipcode" class="mt-1 field_no-errors block w-full shadow-sm sm:text-sm rounded-md" />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="hidden sm:block" aria-hidden="true">
      <div class="py-5">
        <div class="border-t border-gray-200" />
      </div>
    </div>

     <!-- Contact Information -->
    <div class="mt-10 sm:mt-0">
      <div class="md:grid md:grid-cols-4 md:gap-6">
        <div class="md:col-span-1">
          <div class="px-4 sm:px-0">
            <h3 class="text-xl font-medium leading-6 text-gray-900">Contact Information</h3>
          </div>
        </div>
        <div class="mt-5 md:mt-0 md:col-span-3">
          <div class="px-4 py-5 bg-white sm:p-6 shadow overflow-hidden sm:rounded-md">
            <div class="grid grid-cols-6 gap-6">
              <div class="col-span-6 sm:col-span-3">
                <label for="contact_first_name" class="block text-sm font-medium text-gray-700">First name</label>
                <input type="text" name="contact_first_name" id="contact_first_name" class="mt-1 field_no-errors block w-full shadow-sm sm:text-sm rounded-md" />
              </div>

              <div class="col-span-6 sm:col-span-3">
                <label for="contact_last_name" class="block text-sm font-medium text-gray-700">Last name</label>
                <input type="text" name="contact_last_name" id="contact_last_name" class="mt-1 field_no-errors block w-full shadow-sm sm:text-sm rounded-md" />
              </div>

              <div class="col-span-6 sm:col-span-5 lg:col-span-3">
                <label for="contact_email" class="block text-sm font-medium text-gray-700">Email address</label>
                <input type="email" name="contact_email" id="contact_email" class="mt-1 field_no-errors block w-full shadow-sm sm:text-sm rounded-md" />
              </div>

              <div class="col-span-4 lg:col-span-2">
                <label for="contact_phone" class="block text-sm font-medium text-gray-700">Phone</label>
                <input type="tel" name="contact_phone" id="contact_phone" class="field_no-errors mt-1 block w-full shadow-sm sm:text-sm rounded-md" />
              </div>

              <div class="col-span-2 lg:col-span-1">
                <label for="contact_ext" class="block text-sm font-medium text-gray-700">Ext.</label>
                <input type="tel" name="contact_ext" id="contact_ext" class="field_no-errors mt-1 block w-full shadow-sm sm:text-sm rounded-md" />
              </div>

            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="hidden sm:block" aria-hidden="true">
      <div class="py-5">
        <div class="border-t border-gray-200" />
      </div>
    </div>

    <div class="mt-5 sm:mt-0 flex justify-end">
      <button type="button" @click="$router.back()" class="bg-white py-2 px-4 border border-gray-300 rounded-md shadow-sm text-lg font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">Cancel</button>
      <button type="submit" class="ml-3 inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-lg font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">Create</button>
    </div>
  </form>
</template>
