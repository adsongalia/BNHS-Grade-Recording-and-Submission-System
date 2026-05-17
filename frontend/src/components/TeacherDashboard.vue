<template>
  <div class="min-h-screen bg-gray-50">
    <nav class="bg-gradient-to-r from-blue-800 to-blue-600 text-white shadow-lg border-b border-blue-500">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-20 items-center">
          <div class="text-2xl font-black tracking-wider flex items-center gap-2"><span class="text-3xl">📘</span> BNHS-SHS <span class="font-light text-blue-200">| Teacher Portal</span></div>
          <div class="flex space-x-4 items-center">
            <span class="text-sm text-blue-200 font-medium mr-4">Welcome, {{ teacherName }}!</span>
            <button @click="showPasswordModal = true" class="text-sm bg-blue-700 px-3 py-1 rounded hover:bg-blue-600 transition-colors duration-300">Change Password</button>
            <button @click="logout" class="text-blue-200 hover:text-white transition-colors duration-300 font-medium">Logout</button>
          </div>
        </div>
      </div>
    </nav>

    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      
      <div class="flex space-x-2 border-b border-gray-200 mb-8 overflow-x-auto pb-1 hide-on-print">
        <button @click="activeTab = 'setup'" :class="[activeTab === 'setup' ? 'bg-blue-600 text-white shadow-md' : 'text-gray-600 hover:bg-gray-100']" class="py-2.5 px-5 rounded-lg font-bold text-sm transition-all duration-300 whitespace-nowrap">
          Class Setup
        </button>
        <button @click="activeTab = 'students'" :class="[activeTab === 'students' ? 'bg-blue-600 text-white shadow-md' : 'text-gray-600 hover:bg-gray-100']" class="py-2.5 px-5 rounded-lg font-bold text-sm transition-all duration-300 whitespace-nowrap">
          Student Registry
        </button>
        <button @click="activeTab = 'grades'" :class="[activeTab === 'grades' ? 'bg-blue-600 text-white shadow-md' : 'text-gray-600 hover:bg-gray-100']" class="py-2.5 px-5 rounded-lg font-bold text-sm transition-all duration-300 whitespace-nowrap">
          Grade Entry
        </button>
        <button @click="activeTab = 'submissions'" :class="[activeTab === 'submissions' ? 'bg-blue-600 text-white shadow-md' : 'text-gray-600 hover:bg-gray-100']" class="py-2.5 px-5 rounded-lg font-bold text-sm transition-all duration-300 whitespace-nowrap">
          Submission Status
        </button>
        <button @click="activeTab = 'adviser'" :class="[activeTab === 'adviser' ? 'bg-indigo-600 text-white shadow-md' : 'text-indigo-600 hover:bg-indigo-50']" class="py-2.5 px-5 rounded-lg font-bold text-sm transition-all duration-300 whitespace-nowrap flex items-center gap-2">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 20H5a2 2 0 01-2-2V6a2 2 0 012-2h10a2 2 0 012 2v1m2 13a2 2 0 01-2-2V7m2 13a2 2 0 002-2V9a2 2 0 00-2-2h-2m-4-3H9M7 16h6M7 8h6v4H7V8z"></path></svg>
          Adviser: Report Cards
        </button>
      </div>

      <transition name="fade" mode="out-in">
        <div :key="activeTab" class="w-full">

          <div v-if="activeTab === 'setup'">
            <header class="mb-6">
              <h2 class="text-2xl font-bold text-gray-900">My Assigned Classes</h2>
              <p class="text-gray-600">Create sections and assign them to your teaching load.</p>
            </header>
            <div v-if="myAdvisorySections.length === 0" class="bg-red-50 border-l-4 border-red-400 p-4 mb-4 text-red-700 rounded-r-md font-medium flex items-center">
              <svg class="w-6 h-6 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path></svg>
              You have not been assigned as a Class Adviser for any sections. Please contact the Principal's Office.
            </div>

            <div v-else-if="!adviserSectionId" class="bg-indigo-50 border-l-4 border-indigo-400 p-4 mb-4 text-indigo-700 rounded-r-md">
              Select your assigned Advisory Section from the dropdown above to aggregate the report cards.
            </div>

            <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div class="bg-white p-6 shadow-sm rounded-xl border border-gray-200 col-span-1 hover:shadow-lg transition-shadow duration-300">
                <h3 class="font-bold text-lg mb-4">Create New Class</h3>
                <form @submit.prevent="createClass" class="space-y-4">
                  <div>
                    <label class="block text-sm font-medium text-gray-700">Grade Level</label>
                    <select v-model.number="newClassForm.level_id" @change="resetSelections" class="mt-1 block w-full border border-gray-300 rounded-md p-2 focus:ring-blue-500 transition-all">
                      <option value="11">Grade 11</option>
                      <option value="12">Grade 12</option>
                    </select>
                  </div>
                  <div>
                    <label class="block text-sm font-medium text-gray-700">Curriculum Subject</label>
                    <select v-model="newClassForm.subject_code" required class="mt-1 block w-full border border-gray-300 rounded-md p-2 focus:ring-blue-500 transition-all">
                      <option value="" disabled>Select Subject...</option>
                      <option v-for="sub in filteredSubjects" :key="sub.Subject_Code" :value="sub.Subject_Code">
                        {{ sub.Subject_Code }} - {{ sub.Subject_Name }}
                      </option>
                    </select>
                  </div>
                  <div>
                    <label class="block text-sm font-medium text-gray-700">Official Section</label>
                    <select v-model="newClassForm.section_name" required class="mt-1 block w-full border border-gray-300 rounded-md p-2 focus:ring-blue-500 transition-all">
                      <option value="" disabled>Select a Section...</option>
                      <option v-for="sec in filteredSections" :key="sec.Section_ID" :value="sec.Section_Name">
                        {{ sec.Section_Name }}
                      </option>
                    </select>
                  </div>
                  <button type="submit" class="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700 hover:-translate-y-0.5 transition-all shadow-sm">Add to My Load</button>
                </form>
              </div>

              <div class="bg-white p-6 shadow-md rounded-2xl border border-gray-200 col-span-2 hover:shadow-lg transition-shadow duration-300">
                <h3 class="font-bold text-lg mb-4">Current Teaching Load</h3>
                <ul class="divide-y divide-gray-200">
                  <li v-if="myClasses.length === 0" class="py-12 text-center">
                    <div class="flex flex-col items-center justify-center space-y-3">
                      <div class="p-4 bg-blue-50 rounded-full mb-2">
                        <svg class="w-10 h-10 text-blue-300" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"></path></svg>
                      </div>
                      <p class="text-lg font-bold text-gray-500">No classes assigned</p>
                      <p class="text-sm text-gray-400">Use the form on the left to add classes to your teaching load.</p>
                    </div>
                  </li>
                  
                  <li v-for="(cls, index) in myClasses" :key="cls.assignment_id" class="py-4 flex justify-between items-center hover:bg-gray-50 px-2 rounded transition-colors duration-200">
                    <div>
                      <p class="font-bold text-gray-900 flex items-center">
                        {{ cls.section_name }}
                        
                        <span v-if="myAdvisorySections.some(sec => sec.Section_ID === cls.section_id)" class="ml-2 bg-amber-100 text-amber-900 text-[10px] uppercase font-extrabold px-2 py-0.5 rounded-full tracking-wide border border-amber-300 shadow-sm flex items-center">
                          ⭐ Advisory
                        </span>
                      </p>
                      <p class="text-sm text-gray-500">Subject: <span class="font-semibold text-gray-700">{{ cls.subject }}</span> | Section ID: {{ cls.section_id }}</p>
                    </div>
                    <div class="flex items-center space-x-4 border-l pl-4 border-gray-200">
                      
                      <span class="bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded-full font-bold border border-blue-200">#{{ index + 1 }}</span>
                      
                      <button @click="removeClass(cls.assignment_id)" class="text-red-500 hover:text-red-800 text-sm font-semibold transition-colors">Remove</button>
                    </div>
                  </li>
                </ul>
              </div>
            </div>
          </div>

          <div v-if="activeTab === 'students'">
            <header class="mb-6 flex justify-between items-center">
              <div class="flex-1 max-w-lg relative">
                <input v-model="searchQuery" type="text" placeholder="Search students by Name or LRN..." class="w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 transition-all" />
              </div>
              <button @click="openModal()" class="ml-4 px-6 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 hover:-translate-y-0.5 shadow-sm transition-all whitespace-nowrap">
                + Enroll Student
              </button>
            </header>

            <div class="bg-white shadow-md rounded-2xl overflow-hidden border border-gray-200">
              <table class="min-w-full divide-y divide-gray-200">
                <thead class="bg-gray-100">
                  <tr>
                    <th class="py-3 px-4 text-left font-bold text-gray-500 tracking-wider">#</th>
                    <th class="py-3 px-4 text-left font-bold text-gray-500 tracking-wider">LRN</th>
                    <th class="py-3 px-4 text-left font-bold text-gray-500 tracking-wider">STUDENT NAME</th>
                    <th class="py-3 px-4 text-left font-bold text-gray-500 tracking-wider">SECTION</th>
                    <th class="py-3 px-4 text-right font-bold text-gray-500 tracking-wider">ACTIONS</th>
                  </tr>
                </thead>
                <tbody class="bg-white divide-y divide-gray-200">
                  <tr v-if="students.length === 0">
                    <td colspan="5" class="px-6 py-16 text-center">
                      <div class="flex flex-col items-center justify-center space-y-3">
                        <div class="p-4 bg-gray-50 rounded-full mb-2">
                          <svg class="w-12 h-12 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"></path></svg>
                        </div>
                        <p class="text-xl font-bold text-gray-500">No students enrolled</p>
                        <p class="text-sm text-gray-400">Add students to begin managing their records.</p>
                      </div>
                    </td>
                  </tr>
                  <tr v-else-if="filteredStudentsRegistry.length === 0">
                    <td colspan="5" class="px-6 py-16 text-center">
                      <p class="text-xl font-bold text-gray-500">No matches found for "{{ searchQuery }}"</p>
                      <p class="text-sm text-gray-400">Try checking the spelling or the LRN.</p>
                    </td>
                  </tr>
                  <tr v-for="(student, index) in filteredStudentsRegistry" :key="student.LRN" class="hover:bg-blue-50 transition-colors duration-150">
                    <td class="px-4 py-2 text-sm text-gray-500 font-bold">{{ index + 1 }}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{{ student.LRN }}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-700">{{ student.Lastname }}, {{ student.Firstname }} {{ student.Middlename || '' }}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-700">{{ student.Section_Name }}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium space-x-4">
                      <button @click="openModal(student)" class="text-blue-600 hover:text-blue-900 transition-colors">Edit</button>
                      <button @click="deleteStudent(student.LRN)" class="text-red-600 hover:text-red-900 transition-colors">Remove</button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <div v-if="activeTab === 'grades'">
            <header class="mb-6 flex justify-between items-center bg-blue-50 p-4 rounded-xl border border-blue-100 shadow-sm hover:shadow-md transition-shadow duration-300">
              <div>
                <div class="flex items-center space-x-3">
                  <h2 class="text-xl font-bold text-gray-900">Quarterly Grades</h2>
                  <span v-if="selectedAssignmentId" class="bg-blue-200 text-blue-800 text-xs px-3 py-1 rounded-full font-bold">
                    Total Students: {{ filteredGradeStudents.length }}
                  </span>
                </div>
                <div class="mt-2 flex items-center space-x-2">
                  <label class="text-sm font-bold text-gray-700">Select Class to Grade:</label>
                  <select v-model="selectedAssignmentId" class="border-gray-300 rounded shadow-sm text-sm p-1 pr-8 focus:ring-blue-500 transition-all">
                    <option :value="null" disabled>-- Choose a class --</option>
                    <option v-for="cls in myClasses" :key="cls.assignment_id" :value="cls.assignment_id">
                      {{ cls.section_name }} ({{ cls.subject }})
                    </option>
                  </select>
                </div>
              </div>
              <button @click="submitGrades" :disabled="!selectedAssignmentId || isSubmitting || isLocked" class="px-6 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 hover:-translate-y-0.5 disabled:opacity-50 disabled:transform-none shadow-sm transition-all font-bold">
                {{ isLocked ? 'Batch Submitted' : 'Submit Grade Batch' }}
              </button>
            </header>

            <div v-if="!selectedAssignmentId" class="bg-yellow-50 border-l-4 border-yellow-400 p-4 mb-4 text-yellow-700 rounded-r-md">
              Please select a class from the dropdown menu above to begin entering grades.
            </div>

            <div v-else class="bg-white shadow-md rounded-2xl overflow-hidden border border-gray-200">
              <table class="min-w-full divide-y divide-gray-200">
                <thead class="bg-gray-100">
                  <tr>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">LRN</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Student Name</th>
                    <th class="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase">{{ activeTerm.semester === '1st' ? 'Q1' : 'Q3' }}</th>
                    <th class="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase">{{ activeTerm.semester === '1st' ? 'Q2' : 'Q4' }}</th>
                    <th class="px-6 py-3 text-center text-xs font-medium text-blue-600 uppercase">Avg</th>
                  </tr>
                </thead>
                <tbody class="bg-white divide-y divide-gray-200">
                  <tr v-if="filteredGradeStudents.length === 0">
                    <td colspan="5" class="px-6 py-16 text-center">
                      <div class="flex flex-col items-center justify-center space-y-3">
                        <div class="p-4 bg-gray-50 rounded-full mb-2">
                          <svg class="w-12 h-12 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4"></path></svg>
                        </div>
                        <p class="text-xl font-bold text-gray-500">No students in this class</p>
                        <p class="text-sm text-gray-400">Head over to the Student Registry to enroll students into this section.</p>
                      </div>
                    </td>
                  </tr>
                  <tr v-for="(student, index) in filteredGradeStudents" :key="student.lrn" class="hover:bg-blue-50 transition-colors duration-150">
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      <span class="text-gray-400 font-bold mr-2">{{ index + 1 }}.</span>{{ student.lrn }}
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{{ student.name }}</td>
                    <td class="py-3 px-4 text-center">
                      <input type="number" v-model.number="student.q1" :disabled="isLocked" min="60" max="100" class="w-16 border rounded px-2 py-1 text-center text-sm disabled:bg-gray-200 disabled:text-gray-500 disabled:cursor-not-allowed transition-colors" :class="(student.q1 !== null && student.q1 !== '' && (student.q1 < 60 || student.q1 > 100)) ? 'border-red-500 bg-red-50 text-red-700 focus:ring-red-500' : 'border-gray-300 focus:ring-blue-500'" />
                    </td>
                    <td class="py-3 px-4 text-center">
                      <input type="number" v-model.number="student.q2" :disabled="isLocked" min="60" max="100" class="w-16 border rounded px-2 py-1 text-center text-sm disabled:bg-gray-200 disabled:text-gray-500 disabled:cursor-not-allowed transition-colors" :class="(student.q2 !== null && student.q2 !== '' && (student.q2 < 60 || student.q2 > 100)) ? 'border-red-500 bg-red-50 text-red-700 focus:ring-red-500' : 'border-gray-300 focus:ring-blue-500'" />
                    </td>
                    <td class="py-3 px-4 text-center font-extrabold text-blue-700">
                      {{ (student.q1 && student.q2) ? ((student.q1 + student.q2) / 2).toFixed(2) : '-' }}
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <div v-if="activeTab === 'submissions'">
            <header class="mb-6">
              <h2 class="text-2xl font-bold text-gray-900">Submission History</h2>
              <p class="text-gray-600">Track the principal's approval status of your submitted grades.</p>
            </header>
            <div class="bg-white shadow-md rounded-2xl overflow-hidden border border-gray-200 p-6 hover:shadow-lg transition-shadow duration-300">
                <div v-if="mySubmissions.length === 0" class="text-center py-12">
                  <div class="flex flex-col items-center justify-center space-y-3">
                    <div class="p-4 bg-gray-50 rounded-full mb-2">
                      <svg class="w-12 h-12 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4"></path></svg>
                    </div>
                    <p class="text-lg font-bold text-gray-500">No submissions yet</p>
                    <p class="text-sm text-gray-400">Submit your grades in the Grade Entry tab to see them here.</p>
                  </div>
                </div>
                <ul v-else class="divide-y divide-gray-200">
                    <li v-for="sub in mySubmissions" :key="sub.Submission_ID" @click="goToGradeEntry(sub.Assignment_ID)" class="py-4 flex justify-between items-center hover:bg-blue-50 px-4 rounded-lg cursor-pointer border border-transparent hover:border-blue-200 transition-colors duration-150">
                        <div>
                            <p class="text-sm font-bold text-gray-900">Batch #{{ sub.Submission_ID }} — {{ sub.Class }}</p>
                            <p class="text-sm text-gray-500">Submitted on: {{ sub.Date_Submitted }}</p>
                        </div>
                        <div class="flex items-center space-x-3">
                            <span :class="sub.Status.includes('Approved') ? 'bg-green-100 text-green-800' : (sub.Status.includes('Returned') ? 'bg-red-100 text-red-800' : 'bg-yellow-100 text-yellow-800')" class="px-3 py-1 inline-flex text-xs font-bold rounded-full shadow-sm">
                                {{ sub.Status }}
                            </span>
                            <button @click.stop="deleteSubmission(sub.Submission_ID)" class="px-3 py-1 bg-red-100 text-red-700 hover:bg-red-200 rounded text-xs font-bold transition-colors shadow-sm">Delete</button>
                        </div>
                    </li>
                </ul>
            </div>
          </div>

          <div v-if="activeTab === 'adviser'">
            <header class="mb-6 flex justify-between items-center bg-indigo-50 p-4 rounded-xl border border-indigo-100 shadow-sm hover:shadow-md transition-shadow duration-300">
              <div>
                <h2 class="text-xl font-bold text-gray-900 text-indigo-900">Consolidated Grades (SF9)</h2>
                <div class="mt-2 flex items-center space-x-2">
                  <label class="text-sm font-bold text-indigo-800">Select Advisory Section:</label>
                  <select v-model="adviserSectionId" @change="fetchReportCards" class="border-indigo-300 rounded shadow-sm text-sm p-1 pr-8 focus:ring-indigo-500 transition-all">
                    <option :value="null" disabled>-- Choose a section --</option>
                    <option v-for="sec in myAdvisorySections" :key="sec.Section_ID" :value="sec.Section_ID">
                      {{ sec.Section_Name }} (Grade {{ sec.Level_ID }})
                    </option>
                  </select>
                </div>
              </div>
              <button @click="printReport" :disabled="!adviserSectionId" class="px-6 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 hover:-translate-y-0.5 disabled:opacity-50 disabled:transform-none shadow-sm transition-all font-bold">
                Print SF9 Document
              </button>
            </header>

            <div v-if="!adviserSectionId" class="bg-indigo-50 border-l-4 border-indigo-400 p-4 mb-4 text-indigo-700 rounded-r-md">
              Select your assigned Advisory Section from the dropdown above to aggregate the report cards.
            </div>

            <div v-else class="bg-white shadow-sm rounded-xl overflow-x-auto border border-gray-200 print-wrapper">
              <div class="print-header hidden mb-6 px-4 pt-6">
                <h1 class="text-2xl font-black uppercase text-black text-center m-0">Bonga National High School</h1>
                <h2 class="text-lg font-bold text-black text-center m-0">Official Consolidated Grades</h2>
                <div class="mt-6 mb-2 text-black text-sm flex justify-between font-bold border-b-2 border-black pb-2">
                  <div>
                    <p>School Year: {{ reportData.school_year }}</p>
                    <p>Advisory Section: {{ sections.find(s => s.Section_ID === adviserSectionId)?.Section_Name || 'Unknown' }}</p>
                  </div>
                  <div class="text-right">
                    <p>Adviser: {{ teacherName }}</p>
                    <p>Principal: {{ reportData.principal_name }}</p>
                  </div>
                </div>
              </div>

              <table class="min-w-full border-collapse border border-gray-300 printable-table">
                <thead class="bg-gray-100">
                  <tr>
                    <th rowspan="2" class="px-3 py-3 text-left text-xs font-bold text-gray-700 uppercase border border-gray-300 align-middle">LRN</th>
                    <th rowspan="2" class="px-3 py-3 text-left text-xs font-bold text-gray-700 uppercase border border-gray-300 align-middle">Student Name</th>
                    <th :colspan="2" v-for="sub in reportData.subjects" :key="sub" class="px-2 py-2 text-center text-xs font-bold text-gray-700 uppercase border border-gray-300">{{ sub }}</th>
                    <th rowspan="2" class="px-3 py-3 text-center text-xs font-bold text-indigo-700 uppercase border border-gray-300 print-bg-none align-middle">Sem 1<br/>Avg</th>
                    <th rowspan="2" class="px-3 py-3 text-center text-xs font-bold text-indigo-700 uppercase border border-gray-300 print-bg-none align-middle">Sem 2<br/>Avg</th>
                  </tr>
                  <tr>
                    <template v-for="sub in reportData.subjects" :key="sub + '-headers'">
                      <th class="px-2 py-1 text-center text-[10px] font-bold text-gray-600 uppercase border border-gray-300 bg-gray-50">1st Sem</th>
                      <th class="px-2 py-1 text-center text-[10px] font-bold text-gray-600 uppercase border border-gray-300 bg-gray-50">2nd Sem</th>
                    </template>
                  </tr>
                </thead>
                <tbody class="bg-white">
                  <tr v-if="reportData.report.length === 0">
                    <td :colspan="reportData.subjects.length * 2 + 4" class="px-6 py-8 text-center text-gray-500 border border-gray-300">No students found in this section.</td>
                  </tr>
                  <tr v-for="student in reportData.report" :key="student.LRN" class="hover:bg-indigo-50 transition-colors duration-150">
                    <td class="px-3 py-2 whitespace-nowrap text-sm text-gray-900 border border-gray-300">{{ student.LRN }}</td>
                    <td class="px-3 py-2 whitespace-nowrap text-sm font-bold text-gray-900 border border-gray-300">{{ student.Name }}</td>
                    
                    <template v-for="sub in reportData.subjects" :key="sub">
                      <template v-if="typeof student.Grades[sub] === 'string'">
                        <td colspan="2" class="px-2 py-2 whitespace-nowrap text-center text-sm border border-gray-300 align-middle"
                            :class="student.Grades[sub] === 'Pending' ? 'text-yellow-600 font-bold' : 'text-red-500 italic'">
                          {{ student.Grades[sub] === 'Missing' ? 'No Grades Submitted' : 'Pending Principal Approval' }}
                        </td>
                      </template>
                      <template v-else>
                        <td class="px-2 py-2 whitespace-nowrap text-sm border border-gray-300 align-top text-gray-900">
                          <div class="flex flex-col space-y-1 w-20 mx-auto">
                            <div class="flex justify-between"><span class="text-gray-500 text-xs">Q1:</span> <span class="font-medium">{{ student.Grades[sub].Q1 }}</span></div>
                            <div class="flex justify-between"><span class="text-gray-500 text-xs">Q2:</span> <span class="font-medium">{{ student.Grades[sub].Q2 }}</span></div>
                          </div>
                        </td>
                        <td class="px-2 py-2 whitespace-nowrap text-sm border border-gray-300 align-top text-gray-900">
                          <div class="flex flex-col space-y-1 w-20 mx-auto">
                            <div class="flex justify-between"><span class="text-gray-500 text-xs">Q3:</span> <span class="font-medium">{{ student.Grades[sub].Q3 }}</span></div>
                            <div class="flex justify-between"><span class="text-gray-500 text-xs">Q4:</span> <span class="font-medium">{{ student.Grades[sub].Q4 }}</span></div>
                          </div>
                        </td>
                      </template>
                    </template>

                    <td class="px-3 py-2 whitespace-nowrap text-center font-bold text-base text-indigo-700 border border-gray-300 print-bg-none align-middle">{{ student.Sem1_Avg }}</td>
                    <td class="px-3 py-2 whitespace-nowrap text-center font-bold text-base text-indigo-700 border border-gray-300 print-bg-none align-middle">{{ student.Sem2_Avg }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

        </div>
      </transition>
    </div>

    <div v-if="showPasswordModal" class="fixed inset-0 bg-slate-500/20 backdrop-blur-md flex items-center justify-center p-4 z-50 transition-opacity">
      <div class="bg-white rounded-xl shadow-2xl max-w-sm w-full p-6 transform transition-transform">
        <h3 class="text-lg font-bold text-gray-900 mb-4">Change Password</h3>
        <form @submit.prevent="changePassword" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700">Current Password</label>
            <div class="relative">
              <input v-model="pwdForm.old_password" :type="showOldPassword ? 'text' : 'password'" required class="mt-1 block w-full border border-gray-300 rounded-md p-2 pr-10 focus:ring-blue-500 transition-all" />
              <button type="button" @click="showOldPassword = !showOldPassword" class="absolute inset-y-0 right-0 pr-3 flex items-center text-gray-400 hover:text-gray-600 focus:outline-none mt-1">
                <svg v-if="!showOldPassword" class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" /><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" /></svg>
                <svg v-else class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21" /></svg>
              </button>
            </div>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700">New Password</label>
            <div class="relative">
              <input v-model="pwdForm.new_password" :type="showNewPassword ? 'text' : 'password'" required class="mt-1 block w-full border border-gray-300 rounded-md p-2 pr-10 focus:ring-blue-500 transition-all" />
              <button type="button" @click="showNewPassword = !showNewPassword" class="absolute inset-y-0 right-0 pr-3 flex items-center text-gray-400 hover:text-gray-600 focus:outline-none mt-1">
                <svg v-if="!showNewPassword" class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" /><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" /></svg>
                <svg v-else class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21" /></svg>
              </button>
            </div>
          </div>
          <div class="mt-6 flex justify-end space-x-3">
            <button type="button" @click="showPasswordModal = false" class="px-4 py-2 border border-gray-300 text-gray-700 hover:bg-gray-50 rounded-md transition-colors">Cancel</button>
            <button type="submit" class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 hover:-translate-y-0.5 shadow-sm transition-all">Update Password</button>
          </div>
        </form>
      </div>
    </div>

    <div v-if="showModal" class="fixed inset-0 bg-slate-500/20 backdrop-blur-md flex items-center justify-center p-4 z-50 transition-opacity">
      <div class="bg-white rounded-xl shadow-2xl max-w-lg w-full p-6 transform transition-transform">
        <h3 class="text-lg font-bold mb-4">{{ isEditing ? 'Edit Student' : 'Enroll Student' }}</h3>
        <form @submit.prevent="saveStudent" class="grid grid-cols-2 gap-4">
          <div class="col-span-2">
            <label class="block text-sm font-medium text-gray-700">LRN (12 Digits)</label>
            <input v-model.number="form.lrn" type="number" required :disabled="isEditing" class="mt-1 block w-full border border-gray-300 rounded-md p-2 disabled:bg-gray-100 focus:ring-blue-500 transition-all" />
          </div>
          <div class="col-span-1">
            <label class="block text-sm font-medium text-gray-700">Last Name</label>
            <input v-model="form.lastname" type="text" required class="mt-1 block w-full border border-gray-300 rounded-md p-2 focus:ring-blue-500 transition-all" />
          </div>
          <div class="col-span-1">
            <label class="block text-sm font-medium text-gray-700">First Name</label>
            <input v-model="form.firstname" type="text" required class="mt-1 block w-full border border-gray-300 rounded-md p-2 focus:ring-blue-500 transition-all" />
          </div>
          <div class="col-span-1">
            <label class="block text-sm font-medium text-gray-700">Middle Name</label>
            <input v-model="form.middlename" type="text" class="mt-1 block w-full border border-gray-300 rounded-md p-2 focus:ring-blue-500 transition-all" />
          </div>
          <div class="col-span-1">
            <label class="block text-sm font-medium text-gray-700">Sex</label>
            <select v-model="form.sex" class="mt-1 block w-full border border-gray-300 rounded-md p-2 focus:ring-blue-500 transition-all">
              <option value="" disabled>Select...</option>
              <option value="M">Male</option>
              <option value="F">Female</option>
            </select>
          </div>
          <div class="col-span-1">
            <label class="block text-sm font-medium text-gray-700">Assigned Section</label>
            <select v-model.number="form.section_id" required class="mt-1 block w-full border border-gray-300 rounded-md p-2 focus:ring-blue-500 transition-all">
              <option value="" disabled>Select a Section...</option>
              <option v-for="section in sections" :key="section.Section_ID" :value="section.Section_ID">
                {{ section.Section_Name }}
              </option>
            </select>
          </div>
          <div class="col-span-1">
            <label class="block text-sm font-medium text-gray-700">Birth Date</label>
            <input v-model="form.birth_date" type="date" class="mt-1 block w-full border border-gray-300 rounded-md p-2 focus:ring-blue-500 transition-all" />
          </div>
          <div class="col-span-2 mt-4 flex justify-end space-x-3">
            <button type="button" @click="showModal = false" class="px-4 py-2 border border-gray-300 rounded-md hover:bg-gray-50 transition-colors">Cancel</button>
            <button type="submit" class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 hover:-translate-y-0.5 shadow-sm transition-all">Save Student</button>
          </div>
        </form>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, reactive, onMounted, onUnmounted, computed, watch } from 'vue';
import { useRouter } from 'vue-router';
import api from '../api';
import { logout as performLogout } from '../auth';

const router = useRouter();
const activeTab = ref('setup'); 
const teacherId = localStorage.getItem('employee_id');
const teacherName = ref(''); // NEW: Holds the teacher's actual name

// NEW: Fetch the teacher's name
const fetchTeacherProfile = async () => {
  try {
    const res = await api.get(`/api/teacher/${teacherId}/profile`);
    teacherName.value = res.data.name;
  } catch (e) { console.error(e); }
};
// --- STATE ---
const myClasses = ref([]);
const subjectsList = ref([]); 
const newClassForm = reactive({ level_id: 11, section_name: '', subject_code: '' });


// --- SYSTEM TERM STATE & API ---
const activeTerm = reactive({ school_year: '', semester: '1st' });

const fetchActiveTerm = async () => {
  try {
    const res = await api.get('/api/settings/term');
    activeTerm.school_year = res.data.school_year;
    activeTerm.semester = res.data.semester;
  } catch (error) {
    console.error("Failed to fetch active term:", error);
  }
};

const students = ref([]);
const sections = ref([]);
// NEW: Filter sections so the teacher ONLY sees what they advise!
const myAdvisorySections = computed(() => {
  return sections.value.filter(sec => sec.Adviser_ID === teacherId);
}); 
const gradeStudents = ref([]); 
const selectedAssignmentId = ref(null);

const mySubmissions = ref([]);
const searchQuery = ref('');
const isSubmitting = ref(false);

const showModal = ref(false);
const isEditing = ref(false);
const form = reactive({ lrn: '', lastname: '', firstname: '', middlename: '', section_id: '', birth_date: '', sex: '' });

const showPasswordModal = ref(false);
const pwdForm = reactive({ old_password: '', new_password: '' });
const showOldPassword = ref(false);
const showNewPassword = ref(false);

const adviserSectionId = ref(null);
const reportData = ref({ subjects: [], report: [], school_year: '', principal_name: '' });

// --- COMPUTED ---
const filteredStudentsRegistry = computed(() => {
  if (!searchQuery.value) return students.value;
  const q = String(searchQuery.value).toLowerCase();
  return students.value.filter(s => 
    String(s.LRN).startsWith(q) || 
    s.Lastname.toLowerCase().includes(q) || 
    s.Firstname.toLowerCase().includes(q) ||
    `${s.Lastname}, ${s.Firstname}`.toLowerCase().includes(q)
  );
});

const filteredGradeStudents = computed(() => {
  if (!selectedAssignmentId.value) return [];
  const targetClass = myClasses.value.find(c => c.assignment_id === selectedAssignmentId.value);
  if (!targetClass) return [];
  return gradeStudents.value.filter(s => s.section_id === targetClass.section_id);
});

const isLocked = computed(() => {
  if (!selectedAssignmentId.value) return false;
  return mySubmissions.value.some(sub => sub.Assignment_ID === selectedAssignmentId.value && !sub.Status.includes('Returned'));
});

watch(selectedAssignmentId, async (newVal) => {
  if (newVal) {
    try {
      const response = await api.get(`/api/teacher/classes/${newVal}/grades`);
      if (response.data.length > 0) {
        gradeStudents.value.forEach(s => {
          const rec = response.data.find(r => r.LRN === s.lrn);
          if (rec) {
            s.q1 = rec.Q1;
            s.q2 = rec.Q2;
          }
        });
      } else {
        const targetClass = myClasses.value.find(c => c.assignment_id === newVal);
        gradeStudents.value.forEach(s => {
          if (s.section_id === targetClass?.section_id) { s.q1 = null; s.q2 = null; }
        });
      }
    } catch (e) { console.error("Failed to fetch existing grades:", e); }
  }
});

const filteredSubjects = computed(() => {
  return subjectsList.value.filter(sub => sub.Level_ID === newClassForm.level_id);
});

const filteredSections = computed(() => {
  return sections.value.filter(sec => sec.Level_ID === newClassForm.level_id);
});

const resetSelections = () => {
  newClassForm.subject_code = '';
  newClassForm.section_name = '';
};

// --- METHODS ---
const fetchSubjects = async () => {
  try {
    const response = await api.get('/api/curriculum/subjects');
    subjectsList.value = response.data;
  } catch(e) { console.error(e); }
};

const fetchMyClasses = async () => {
  try {
    const response = await api.get(`/api/teacher/${teacherId}/classes`);
    myClasses.value = response.data;
  } catch(e) { console.error(e); }
};

const createClass = async () => {
  try {
    await api.post(`/api/teacher/${teacherId}/setup-class`, newClassForm);
    alert("Class successfully added to your load!");
    newClassForm.section_name = ''; 
    fetchMyClasses();
  } catch (error) { 
    alert(error.response?.data?.detail || error.message); 
  }
};

const removeClass = async (assignmentId) => {
  if (confirm(`Are you sure you want to remove Assignment #${assignmentId} from your teaching load?`)) {
    try {
      await api.delete(`/api/teacher/classes/${assignmentId}`);
      fetchMyClasses(); 
    } catch (error) { 
      alert(error.response?.data?.detail || error.message); 
    }
  }
};

const changePassword = async () => {
  try {
    await api.post(`/api/auth/change-password/${teacherId}`, pwdForm);
    alert("Password changed successfully!");
    showPasswordModal.value = false;
    pwdForm.old_password = ''; pwdForm.new_password = '';
  } catch (e) { 
    alert(e.response?.data?.detail || "Error: Incorrect old password."); 
  }
};

const logout = () => {
  performLogout();
};

const fetchMySubmissions = async () => {
  try {
    const response = await api.get(`/api/teacher/my-submissions/${teacherId}`);
    mySubmissions.value = response.data;
  } catch(e) { console.error(e); }
};

const submitGrades = async () => {
  if (filteredGradeStudents.value.length < 10) {
      alert("❌ PDF Constraint Failed: A section must have a minimum of 10 enrolled students before an official grade batch can be submitted.");
      return;
  }
  const hasEmpty = filteredGradeStudents.value.some(s => !s.q1 || !s.q2);
  if (hasEmpty) {
      alert("❌ You must encode Q1 and Q2 grades for ALL students in this section before submitting.");
      return;
  }

  const hasInvalid = filteredGradeStudents.value.some(s => s.q1 < 60 || s.q1 > 100 || s.q2 < 60 || s.q2 > 100);
  if (hasInvalid) {
      alert("❌ Invalid grades detected. All grades must be between 60 and 100.");
      return;
  }

  isSubmitting.value = true;
  const payload = {
    teacher_assignment_id: selectedAssignmentId.value, 
    grades: filteredGradeStudents.value.map(s => ({ lrn: s.lrn, q1: s.q1, q2: s.q2 }))
  };
  
  try {
    await api.post('/api/teacher/submit-grades', payload);
    alert("✅ Grade batch successfully submitted to Principal!");
    fetchMySubmissions(); 
  } catch (error) { 
    alert(error.response?.data?.detail || "Error submitting grades"); 
    console.error(error); 
  }
  finally { isSubmitting.value = false; }
};

const deleteSubmission = async (id) => {
  if (confirm("Are you sure you want to completely delete this grade submission? You will need to encode the grades again.")) {
    try {
      // Clear active grade entry if it's the deleted class
      const sub = mySubmissions.value.find(s => s.Submission_ID === id);
      if (sub && selectedAssignmentId.value === sub.Assignment_ID) {
        gradeStudents.value.forEach(s => { s.q1 = null; s.q2 = null; });
      }
      await api.delete(`/api/teacher/submissions/${id}`);
      fetchMySubmissions();
    } catch (error) {
      alert(error.response?.data?.detail || "Error deleting submission");
    }
  }
};

const clampGrade = (student, quarter) => {
  if (student[quarter] > 100) student[quarter] = 100;
  if (student[quarter] < 0) student[quarter] = null;
};

const goToGradeEntry = (assignmentId) => {
  selectedAssignmentId.value = assignmentId;
  activeTab.value = 'grades';
};

const calculateAvg = (q1, q2) => (q1 && q2) ? ((q1 + q2) / 2).toFixed(2) : '-';

const fetchReportCards = async () => {
  if (!adviserSectionId.value) return;
  try {
    const response = await api.get(`/api/adviser/report-cards/${adviserSectionId.value}`);
    reportData.value = response.data;
  } catch(e) { console.error(e); }
};

const printReport = () => { window.print(); };

const fetchSections = async () => {
  try {
    const response = await api.get('/api/principal/sections');
    sections.value = response.data;
  } catch(e) { console.error(e); }
};

const fetchStudents = async () => {
  const url = searchQuery.value ? `/api/teacher/students?search=${searchQuery.value}` : '/api/teacher/students';
  try {
    const response = await api.get(url);
    const data = response.data;
    students.value = data.sort((a, b) => a.Lastname.localeCompare(b.Lastname));
    students.value = data;

    gradeStudents.value = data.map(s => {
      const existing = gradeStudents.value.find(gs => gs.lrn === s.LRN);
      return {
        lrn: s.LRN, section_id: s.Section_ID, name: `${s.Lastname}, ${s.Firstname} ${s.Middlename || ''}`.trim(),
        q1: existing ? existing.q1 : null, q2: existing ? existing.q2 : null
      };
    });
  } catch(e) { console.error(e); }
};

const openModal = (student = null) => {
  if (student) {
    isEditing.value = true;
    Object.assign(form, { lrn: student.LRN, lastname: student.Lastname, firstname: student.Firstname, middlename: student.Middlename || '', section_id: student.Section_ID, birth_date: student.Birth_Date || '', sex: student.Sex || '' });
  } else {
    isEditing.value = false;
    Object.assign(form, { lrn: '', lastname: '', firstname: '', middlename: '', section_id: '', birth_date: '', sex: '' });
  }
  showModal.value = true;
};

const saveStudent = async () => {
  try {
      const payload = { ...form };
      if (!payload.birth_date) payload.birth_date = null;
      if (!payload.middlename) payload.middlename = null;
      if (!payload.sex) payload.sex = null;

      if (isEditing.value) {
        await api.put(`/api/teacher/students/${form.lrn}`, payload);
      } else {
        await api.post('/api/teacher/students', payload);
      }
      showModal.value = false;
      fetchStudents(); 
  } catch (error) { 
    alert(error.response?.data?.detail || "Failed to save student."); 
  }
};

const deleteStudent = async (lrn) => {
  if (confirm(`Delete student ${lrn}?`)) {
    try {
      await api.delete(`/api/teacher/students/${lrn}`);
      fetchStudents(); 
    } catch (error) {
      alert(error.response?.data?.detail || "Failed to delete student.");
    }
  }
};

let pollInterval;
onMounted(() => {
  fetchTeacherProfile();
  fetchSubjects(); fetchMyClasses(); fetchStudents(); fetchSections(); fetchMySubmissions(); fetchActiveTerm();
  pollInterval = setInterval(() => {
    fetchMySubmissions();
    if (adviserSectionId.value) fetchReportCards();
  }, 3000);
});
onUnmounted(() => clearInterval(pollInterval));
</script>

<style scoped>
/* VUE TRANSITION ANIMATIONS */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.25s ease-out, transform 0.25s ease-out;
}

.fade-enter-from {
  opacity: 0;
  transform: translateY(10px);
}

.fade-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

/* CSS FOR OFFICIAL DOCUMENT PRINTING */
@media print {
  /* Set standard paper margins and hide browser URL/Date headers */
  @page {
    margin: 0.5in;
    size: auto;
  }

  /* Hide all web UI elements */
  nav, button, select, header, .bg-yellow-50, .bg-indigo-50, .bg-red-50, .hide-on-print {
    display: none !important;
  }

  /* Force pure white backgrounds */
  body, .min-h-screen, .bg-gray-50, .print-wrapper, table, th, td {
    background-color: white !important;
  }

  .max-w-7xl {
    max-width: 100% !important;
    padding: 0 !important;
    margin: 0 !important;
  }

  .print-wrapper {
    border: none !important;
    box-shadow: none !important;
    border-radius: 0 !important;
    overflow: visible !important;
  }

  .print-header {
    display: block !important;
  }

  .printable-table {
    width: 100% !important;
    border-collapse: collapse !important;
  }

  .printable-table th, .printable-table td {
    border: 1px solid black !important;
    color: black !important;
    padding: 8px 12px !important;
    white-space: nowrap !important;
  }

  .print-bg-none {
    background-color: transparent !important;
  }
}
</style>