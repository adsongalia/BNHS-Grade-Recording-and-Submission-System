<template>
  <div class="relative min-h-screen flex items-center justify-center bg-slate-900 overflow-hidden">
    <!-- Animated Background Shapes -->
    <div class="absolute top-[-10%] left-[-10%] w-96 h-96 bg-blue-500 rounded-full mix-blend-multiply filter blur-[100px] opacity-30 animate-blob"></div>
    <div class="absolute top-[20%] right-[-10%] w-96 h-96 bg-purple-500 rounded-full mix-blend-multiply filter blur-[100px] opacity-30 animate-blob animation-delay-2000"></div>
    <div class="absolute bottom-[-20%] left-[20%] w-96 h-96 bg-indigo-500 rounded-full mix-blend-multiply filter blur-[100px] opacity-30 animate-blob animation-delay-4000"></div>

    <div class="max-w-md w-full relative z-10 px-8 py-10 bg-white/10 backdrop-blur-xl rounded-3xl shadow-[0_8px_32px_0_rgba(0,0,0,0.3)] border border-white/20">
      <div class="text-center mb-8">
        <div class="w-20 h-20 bg-white rounded-full flex items-center justify-center mx-auto mb-5 shadow-lg transform transition-transform hover:scale-105 duration-300">
          <span class="text-4xl">🎓</span>
        </div>
        <h2 class="text-3xl font-black text-white tracking-wide">BNHS<span class="font-light text-blue-200">-SHS</span></h2>
        <p class="text-blue-200 mt-2 text-sm font-medium">Log in to your account</p>
      </div>

      <form @submit.prevent="handleLogin" class="space-y-6">
        <div v-if="errorMsg" class="bg-red-500/20 border border-red-500/50 text-red-100 px-4 py-3 rounded-xl text-sm font-medium flex items-center animate-fade-in">
          <svg class="w-5 h-5 mr-2 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd"></path></svg>
          {{ errorMsg }}
        </div>

        <div class="space-y-1">
          <label class="block text-xs font-bold text-blue-100 uppercase tracking-wider">Employee ID</label>
          <div class="relative group">
            <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-blue-300 group-focus-within:text-white transition-colors">
              <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path></svg>
            </div>
            <input v-model="form.employeeId" type="text" required class="block w-full pl-10 pr-3 py-3.5 border border-white/20 rounded-xl leading-5 bg-black/20 text-white placeholder-blue-300/50 focus:outline-none focus:ring-2 focus:ring-blue-400 focus:border-transparent transition-all sm:text-sm shadow-inner" placeholder="Enter your ID" />
          </div>
        </div>

        <div class="space-y-1">
          <label class="block text-xs font-bold text-blue-100 uppercase tracking-wider">Password</label>
          <div class="relative group">
            <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-blue-300 group-focus-within:text-white transition-colors">
              <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"></path></svg>
            </div>
            <input v-model="form.password" :type="showPassword ? 'text' : 'password'" required class="block w-full pl-10 pr-10 py-3.5 border border-white/20 rounded-xl leading-5 bg-black/20 text-white placeholder-blue-300/50 focus:outline-none focus:ring-2 focus:ring-blue-400 focus:border-transparent transition-all sm:text-sm shadow-inner" placeholder="••••••••" />
            <button type="button" @click="showPassword = !showPassword" class="absolute inset-y-0 right-0 pr-3 flex items-center text-blue-300 hover:text-white transition-colors focus:outline-none">
              <svg v-if="!showPassword" class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" /><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" /></svg>
              <svg v-else class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21" /></svg>
            </button>
          </div>
        </div>

        <button type="submit" :disabled="isLoading" class="w-full flex justify-center py-3.5 px-4 border border-transparent rounded-xl shadow-lg text-sm font-bold text-blue-900 bg-white hover:bg-blue-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 focus:ring-offset-transparent disabled:opacity-70 transition-all duration-300 hover:-translate-y-1 mt-6">
          <svg v-if="isLoading" class="animate-spin -ml-1 mr-3 h-5 w-5 text-blue-900" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          {{ isLoading ? 'Authenticating...' : 'Sign In' }}
        </button>
      </form>
      
      <div class="mt-8 text-center text-xs text-blue-200/60 font-medium">
        &copy; 2025 Bonga National High School - Senior High School.<br />All rights reserved.
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { login } from '../auth.js';

const router = useRouter();
const form = reactive({ employeeId: '', password: '' });
const errorMsg = ref('');
const isLoading = ref(false);
const showPassword = ref(false);
const isChecking = ref(true);

onMounted(() => {
  // Prevent auto-login on shared devices by clearing any leftover session 
  // when explicitly visiting the login view.
  localStorage.removeItem('access_token');
  localStorage.removeItem('user_role');
  isChecking.value = false;
});

const handleLogin = async () => {
  errorMsg.value = '';
  isLoading.value = true;
  
  const result = await login(form.employeeId, form.password);
  
  if (result.success) {
    if (result.role === 'Principal') {
      router.replace('/principal-dashboard');
    } else {
      router.replace('/teacher-dashboard');
    }
  } else {
    errorMsg.value = result.error;
    isLoading.value = false;
  }
};
</script>

<style>
@keyframes blob {
  0% { transform: translate(0px, 0px) scale(1); }
  33% { transform: translate(30px, -50px) scale(1.1); }
  66% { transform: translate(-20px, 20px) scale(0.9); }
  100% { transform: translate(0px, 0px) scale(1); }
}
.animate-blob {
  animation: blob 7s infinite;
}
.animation-delay-2000 {
  animation-delay: 2s;
}
.animation-delay-4000 {
  animation-delay: 4s;
}
.animate-fade-in {
  animation: fadeIn 0.3s ease-out;
}
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(-10px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>
