<template>
  <NavigationBar>
    <RouterView />
  </NavigationBar>
</template>

<script>
import NavigationBar from './components/NavigationBar.vue'

export default {
  components: {
    NavigationBar,
  },
}
</script>
