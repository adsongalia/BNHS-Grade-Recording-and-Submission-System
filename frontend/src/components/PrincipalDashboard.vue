<template>
  <div class="min-h-screen bg-gray-50">
    <nav class="bg-gradient-to-r from-blue-900 to-indigo-900 text-white shadow-lg border-b border-indigo-700">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-20 items-center">
          <div class="text-2xl font-black tracking-wider flex items-center gap-3"><span class="text-3xl">🏛️</span> BNHS-SHS <span class="font-light text-blue-300">| Principal's Office</span></div>
          <div class="flex space-x-4 items-center">
            <span class="text-sm text-blue-200 font-medium mr-4">Welcome, {{ principalName }}</span>
            <button @click="showProfileModal = true" class="text-sm bg-blue-700 px-3 py-1 rounded hover:bg-blue-600 transition-colors duration-300 shadow-sm">My Profile</button>
            <button @click="logout" class="text-blue-200 hover:text-white transition-colors duration-300 font-medium">Logout</button>
          </div>
        </div>
      </div>
    </nav>

    <div class="max-w-7xl mx-auto px-4 py-8">

      <div class="flex space-x-2 border-b border-gray-200 mb-8 overflow-x-auto pb-1">
        <button @click="activeTab = 'overview'" :class="[activeTab === 'overview' ? 'bg-blue-600 text-white shadow-md' : 'text-gray-600 hover:bg-gray-100']" class="py-2.5 px-5 rounded-lg font-bold text-sm transition-all duration-300 whitespace-nowrap">Dashboard Overview</button>
        <button @click="activeTab = 'approvals'" :class="[activeTab === 'approvals' ? 'bg-blue-600 text-white shadow-md' : 'text-gray-600 hover:bg-gray-100']" class="py-2.5 px-5 rounded-lg font-bold text-sm transition-all duration-300 whitespace-nowrap">Grade Approvals</button>
        <button @click="activeTab = 'teachers'" :class="[activeTab === 'teachers' ? 'bg-blue-600 text-white shadow-md' : 'text-gray-600 hover:bg-gray-100']" class="py-2.5 px-5 rounded-lg font-bold text-sm transition-all duration-300 whitespace-nowrap">Teacher Management</button>
        <button @click="activeTab = 'curriculum'" :class="[activeTab === 'curriculum' ? 'bg-blue-600 text-white shadow-md' : 'text-gray-600 hover:bg-gray-100']" class="py-2.5 px-5 rounded-lg font-bold text-sm transition-all duration-300 whitespace-nowrap">Curriculum Setup</button>
      </div>

      <transition name="fade" mode="out-in">
        <div :key="activeTab" class="w-full">
          
          <div v-if="activeTab === 'overview'" class="space-y-6">
            <div class="bg-blue-50 border border-blue-200 rounded-lg p-5 flex justify-between items-center shadow-sm">
              <div>
                <h2 class="text-lg font-extrabold text-blue-900">Active Academic Term</h2>
                <p class="text-sm text-blue-700 mt-1">All new classes, sections, and grades will be recorded under this term.</p>
              </div>
              <div class="flex space-x-4">
                <div>
                  <p class="text-xs font-bold text-blue-800 uppercase tracking-wider mb-1">School Year</p>
                  <input v-model="activeTerm.school_year" type="text" class="border border-blue-300 rounded px-3 py-2 text-sm font-semibold text-gray-800 focus:ring-blue-500 w-32 shadow-inner" />
                </div>
                <div>
                  <p class="text-xs font-bold text-blue-800 uppercase tracking-wider mb-1">Semester</p>
                  <select v-model="activeTerm.semester" class="border border-blue-300 rounded px-3 py-2 text-sm font-semibold text-gray-800 focus:ring-blue-500 w-24 shadow-inner">
                    <option value="1st">1st</option>
                    <option value="2nd">2nd</option>
                  </select>
                </div>
                <div class="flex items-end">
                  <button @click="saveActiveTerm" class="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-5 rounded transition-all shadow text-sm">Apply System Wide</button>
                </div>
              </div>
            </div>

            <div class="bg-red-50 border border-red-200 rounded-lg p-5 flex justify-between items-center shadow-sm mt-4">
              <div>
                <h2 class="text-lg font-extrabold text-red-900">End of School Year / Archiving</h2>
                <p class="text-sm text-red-700 mt-1">Saves all current student section assignments to the historical archive and clears sections for the new year.</p>
              </div>
              <button @click="archiveSchoolYear" class="bg-red-600 hover:bg-red-700 text-white font-bold py-2 px-5 rounded transition-all shadow text-sm whitespace-nowrap">Archive & Advance Year</button>
            </div>

            <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
              
              <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-lg hover:-translate-y-1 transition-all duration-300">
                <div class="flex justify-between items-start mb-4">
                  <div class="p-3 rounded-full bg-blue-100 text-blue-600 transition-transform duration-500 hover:scale-110">
                    <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"></path></svg>
                  </div>
                  <select v-model="studentStatFilter" class="text-xs border-gray-300 rounded text-gray-600 focus:ring-blue-500 p-1">
                    <option value="ALL">All Grades</option>
                    <option value="11">Grade 11</option>
                    <option value="12">Grade 12</option>
                  </select>
                </div>
                <div>
                  <p class="text-sm text-gray-500 font-medium uppercase tracking-wide">Total Enrolled</p>
                  <p class="text-3xl font-bold text-gray-900">{{ displayedStudentCount }} <span class="text-sm font-normal text-gray-500">Students</span></p>
                </div>
              </div>

              <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6 flex items-center hover:shadow-lg hover:-translate-y-1 transition-all duration-300">
                <div class="p-3 rounded-full bg-indigo-100 text-indigo-600 mr-4 transition-transform duration-500 hover:scale-110">
                  <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path></svg>
                </div>
                <div>
                  <p class="text-sm text-gray-500 font-medium uppercase tracking-wide">Faculty</p>
                  <p class="text-3xl font-bold text-gray-900">{{ stats.teachers }} <span class="text-sm font-normal text-gray-500">Teachers</span></p>
                </div>
              </div>

              <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6 flex items-center hover:shadow-lg hover:-translate-y-1 transition-all duration-300">
                <div class="p-3 rounded-full bg-purple-100 text-purple-600 mr-4 transition-transform duration-500 hover:scale-110">
                  <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"></path></svg>
                </div>
                <div>
                  <p class="text-sm text-gray-500 font-medium uppercase tracking-wide">Curriculum</p>
                  <p class="text-3xl font-bold text-gray-900">{{ stats.sections }} <span class="text-sm font-normal text-gray-500">Active Sections</span></p>
                </div>
              </div>
            </div>

            <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow duration-300">
              <h3 class="text-lg font-bold text-gray-900 mb-2">Grading Period Progress</h3>
              <p class="text-sm text-gray-600 mb-6">Track the official approval status of submitted grade batches across all teachers.</p>
              <div class="flex justify-between items-end mb-2">
                <div>
                  <span class="text-3xl font-bold text-green-600">{{ stats.submissions.rate }}%</span>
                  <span class="text-gray-500 ml-2 font-medium">Approved</span>
                </div>
                <div class="text-right text-sm">
                  <p class="font-bold text-gray-700">{{ stats.submissions.approved }} / {{ stats.submissions.total }} Batches</p>
                  <p class="text-red-500">{{ stats.submissions.pending }} Pending Review</p>
                </div>
              </div>
              <div class="w-full bg-gray-200 rounded-full h-4 mb-4 overflow-hidden">
                <div class="bg-green-500 h-4 transition-all duration-1000 ease-out" :style="{ width: stats.submissions.rate + '%' }"></div>
              </div>
            </div>
          </div>

          <div v-if="activeTab === 'approvals'">
            <div class="flex justify-between items-center mb-4">
              <h2 class="text-xl font-bold text-gray-900">Grade Submissions</h2>
              <select v-model="approvalFilter" class="border border-gray-300 rounded-md shadow-sm text-sm p-2 focus:ring-blue-500 font-medium bg-white">
                <option value="Pending">Pending Review</option>
                <option value="Approved">Approved (Archived)</option>
              </select>
            </div>

            <div v-if="stats.submissions.pending === 0 && approvalFilter === 'Pending'" class="mb-6 bg-gradient-to-r from-emerald-50 to-teal-50 border-l-4 border-emerald-500 p-5 rounded-r-xl shadow-sm flex items-center transform transition-all hover:scale-[1.01] duration-300">
              <div class="p-3 bg-emerald-100 rounded-full mr-4">
                <svg class="w-8 h-8 text-emerald-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
              </div>
              <div>
                <h3 class="text-emerald-900 font-extrabold text-lg tracking-wide">All Caught Up!</h3>
                <p class="text-emerald-700 font-medium mt-0.5">There are no pending grade submissions requiring your approval at the moment.</p>
              </div>
            </div>
            
            <div class="bg-white shadow-md rounded-xl overflow-hidden border border-gray-200">
              <table class="min-w-full divide-y divide-gray-200">
                <thead class="bg-gray-100">
                  <tr>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Batch ID</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Date Submitted</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Teacher & Class</th>
                    <th class="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase">Status</th>
                    <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">Actions</th>
                  </tr>
                </thead>
                <tbody class="bg-white divide-y divide-gray-200">
                  <tr v-if="filteredSubmissions.length === 0">
                    <td colspan="5" class="px-6 py-16 text-center">
                      <div class="flex flex-col items-center justify-center space-y-3">
                        <div class="p-4 bg-gray-50 rounded-full mb-2">
                          <svg class="w-12 h-12 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path></svg>
                        </div>
                        <p class="text-xl font-bold text-gray-500">No {{ approvalFilter.toLowerCase() }} submissions</p>
                        <p class="text-sm text-gray-400 max-w-sm">There are currently no submissions matching this filter.</p>
                      </div>
                    </td>
                  </tr>
                  <tr v-for="sub in filteredSubmissions" :key="sub.Submission_ID" class="hover:bg-gray-50 transition-colors duration-150">
                    <td class="px-6 py-4 text-sm text-gray-900 font-bold">#{{ sub.Submission_ID }}</td>
                    <td class="px-6 py-4 text-sm text-gray-700">{{ sub.Date_Submitted }}</td>
                    <td class="px-6 py-4 text-sm">
                      <div class="font-medium text-gray-900">{{ sub.Teacher }}</div>
                      <div class="text-gray-500">{{ sub.Subject }} ({{ sub.Section }})</div>
                    </td>
                    <td class="px-6 py-4 text-center">
                      <span :class="sub.Status === 'Approved' ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'" class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full">{{ sub.Status }}</span>
                    </td>
                    <td class="px-6 py-4 text-right space-x-2">
                      <button @click="viewGrades(sub.Submission_ID)" class="px-3 py-1.5 bg-blue-100 text-blue-700 font-bold rounded-md text-sm hover:bg-blue-200 hover:-translate-y-0.5 transition-all shadow-sm">Inspect</button>
                      <template v-if="sub.Status === 'Pending'">
                        <button @click="approveBatch(sub.Submission_ID)" class="px-3 py-1.5 bg-green-600 text-white font-bold rounded-md text-sm hover:bg-green-700 hover:-translate-y-0.5 transition-all shadow-sm">Approve</button>
                        <button @click="rejectBatch(sub.Submission_ID)" class="px-3 py-1.5 bg-yellow-100 text-yellow-700 font-bold rounded-md text-sm hover:bg-yellow-200 hover:-translate-y-0.5 transition-all shadow-sm">Return</button>
                      </template>
                      <template v-if="sub.Status === 'Approved'">
                        <button @click="exportGrades(sub.Submission_ID)" class="px-3 py-1.5 bg-indigo-600 text-white font-bold rounded-md text-sm hover:bg-indigo-700 hover:-translate-y-0.5 transition-all shadow-sm">Export CSV</button>
                      </template>
                      <button @click="deleteSubmission(sub.Submission_ID)" class="px-3 py-1.5 bg-red-100 text-red-700 font-bold rounded-md text-sm hover:bg-red-200 hover:-translate-y-0.5 transition-all shadow-sm">Delete</button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <div v-if="activeTab === 'teachers'">
            <header class="mb-4 flex justify-between items-center">
              <h2 class="text-2xl font-bold text-gray-900">Faculty Roster</h2>
              <button @click="openTeacherModal()" class="px-6 py-2.5 font-bold bg-blue-600 text-white rounded-lg hover:bg-blue-700 hover:-translate-y-0.5 shadow-md transition-all">+ Add New Teacher</button>
            </header>
            <div class="bg-white shadow-md rounded-xl overflow-hidden border border-gray-200">
              <table class="min-w-full divide-y divide-gray-200">
                <thead class="bg-gray-100">
                  <tr>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Employee ID</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Last Name</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">First Name</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Role</th>
                    <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">Actions</th>
                  </tr>
                </thead>
                <tbody class="bg-white divide-y divide-gray-200">
                  <tr v-if="teachers.length === 0">
                    <td colspan="5" class="px-6 py-16 text-center">
                      <div class="flex flex-col items-center justify-center space-y-3">
                        <div class="p-4 bg-gray-50 rounded-full mb-2">
                          <svg class="w-12 h-12 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"></path></svg>
                        </div>
                        <p class="text-xl font-bold text-gray-500">No teachers found</p>
                        <p class="text-sm text-gray-400">Click the button above to add faculty members to the system.</p>
                      </div>
                    </td>
                  </tr>
                  <tr v-for="teacher in teachers" :key="teacher.Teacher_ID" class="hover:bg-gray-50 transition-colors duration-150">
                    <td class="px-6 py-4 text-sm text-gray-900 font-bold">{{ teacher.Employee_ID }}</td>
                    <td class="px-6 py-4 text-sm text-gray-700">{{ teacher.Lastname }}</td>
                    <td class="px-6 py-4 text-sm text-gray-700">{{ teacher.Firstname }}</td>
                    <td class="px-6 py-4 text-sm text-gray-700">
                      <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-blue-100 text-blue-800">{{ teacher.Teacher_Type || 'Subject Teacher' }}</span>
                    </td>
                    <td class="px-6 py-4 text-right space-x-4">
                      <button @click="openTeacherModal(teacher)" class="text-blue-600 hover:text-blue-900 text-sm font-medium transition-colors">Edit</button>
                      <button @click="deleteTeacher(teacher.Teacher_ID)" class="text-red-600 hover:text-red-900 text-sm font-medium transition-colors">Remove</button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <div v-if="activeTab === 'curriculum'" class="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <div class="bg-white shadow-sm rounded-xl border border-gray-200 p-6 hover:shadow-md transition-shadow duration-300">
              <h3 class="text-xl font-bold text-gray-900 mb-4">SHS Strands</h3>
              <form @submit.prevent="saveStrand" class="space-y-3 mb-6">
                <input v-model="strandForm.track_name" type="text" placeholder="Track (e.g. Academic, TVL)" required class="w-full border border-gray-300 rounded p-2 text-sm focus:ring-blue-500 transition-all" />
                <div class="flex space-x-2">
                  <input v-model="strandForm.strand_code" type="text" placeholder="Code (e.g. STEM)" required class="w-1/3 border border-gray-300 rounded p-2 text-sm focus:ring-blue-500 transition-all" />
                  <input v-model="strandForm.strand_name" type="text" placeholder="Full Name" required class="w-2/3 border border-gray-300 rounded p-2 text-sm focus:ring-blue-500 transition-all" />
                </div>
                <div class="flex space-x-2">
                  <button type="submit" class="flex-1 bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition-all shadow-sm">{{ isEditingSubject ? 'Update Subject' : 'Add Subject' }}</button>
                  <button v-if="isEditingSubject" @click="cancelEditSubject" type="button" class="w-1/3 bg-gray-200 text-gray-800 px-4 py-2 rounded hover:bg-gray-300 transition-all shadow-sm font-medium">Cancel</button>
                </div>
              </form>
              <ul class="divide-y divide-gray-200 max-h-96 overflow-y-auto">
                <li v-for="str in strands" :key="str.Strand_ID" class="py-3 flex justify-between items-center hover:bg-gray-50 px-2 rounded transition-colors">
                  <div>
                    <p class="font-bold text-sm text-gray-900">{{ str.Strand_Code }} <span class="text-xs text-gray-500 font-normal border ml-1 px-1 rounded">{{ str.Track_Name }}</span></p>
                    <p class="text-xs text-gray-600">{{ str.Strand_Name }}</p>
                  </div>
                  <button @click="deleteStrand(str.Strand_ID)" class="text-red-500 hover:text-red-700 text-xs font-bold transition-colors">Del</button>
                </li>
              </ul>
            </div>
            <div class="bg-white shadow-sm rounded-xl border border-gray-200 p-6 hover:shadow-md transition-shadow duration-300">
              <div class="flex justify-between items-center mb-4">
                <h3 class="text-xl font-bold text-gray-900">Sections</h3>
                <select v-model="sectionFilter" class="border border-gray-300 rounded text-sm p-1 text-gray-700 font-medium bg-gray-50 hover:bg-gray-100 cursor-pointer outline-none focus:ring-blue-500">
                  <option value="ALL">All</option><option value="11">Gr. 11</option><option value="12">Gr. 12</option>
                </select>
              </div>
              <form @submit.prevent="saveSection" class="space-y-3 mb-6">
                <input v-model="sectionForm.section_name" type="text" placeholder="Section Name (e.g. 11-Darwin)" required class="w-full border border-gray-300 rounded p-2 text-sm focus:ring-blue-500 transition-all" />
                <div class="flex space-x-2">
                  <select v-model.number="sectionForm.level_id" class="w-1/3 border border-gray-300 rounded p-2 text-sm focus:ring-blue-500 transition-all">
                    <option value="11">Gr. 11</option><option value="12">Gr. 12</option>
                  </select>
                  <select v-model.number="sectionForm.strand_id" required class="w-2/3 border border-gray-300 rounded p-2 text-sm focus:ring-blue-500 transition-all">
                    <option value="" disabled>Assign Strand...</option>
                    <option v-for="str in strands" :key="str.Strand_ID" :value="str.Strand_ID">{{ str.Strand_Code }}</option>
                  </select>
                </div>
                <select v-model="sectionForm.adviser_id" class="w-full border border-gray-300 rounded p-2 text-sm focus:ring-blue-500 transition-all bg-indigo-50">
                  <option value="">-- Assign Class Adviser (Optional) --</option>
                  <option v-for="adv in availableAdvisers" :key="adv.Employee_ID" :value="adv.Employee_ID">{{ adv.Lastname }}, {{ adv.Firstname }}</option>
                </select>
                <button type="submit" class="w-full bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition-all shadow-sm">Add Section</button>
              </form>
              <ul class="divide-y divide-gray-200 max-h-96 overflow-y-auto">
                <li v-if="filteredAndSortedSections.length === 0" class="py-4 text-sm text-gray-500 text-center">No sections found for this filter.</li>
                <li v-for="sec in filteredAndSortedSections" :key="sec.Section_ID" class="py-3 flex flex-col hover:bg-gray-50 px-2 rounded transition-colors">
                  <div class="flex justify-between items-start w-full">
                    <div>
                      <p class="font-bold text-sm text-gray-900">{{ sec.Section_Name }}</p>
                      <p class="text-xs text-gray-500">Gr. {{ sec.Level_ID }} | Strand: {{ strands.find(s => s.Strand_ID === sec.Strand_ID)?.Strand_Code || sec.Strand_ID }}</p>
                    </div>
                    <button @click="deleteSection(sec.Section_ID)" class="text-red-500 hover:text-red-700 text-xs font-bold transition-colors ml-2">Del</button>
                  </div>
                  <div class="mt-2 flex items-center justify-between bg-indigo-50 px-2 py-1 rounded border border-indigo-100">
                    <span class="text-xs font-bold text-indigo-800">Adviser: {{ sec.Adviser_Name }}</span>
                    <select :value="sec.Adviser_ID || ''" @change="assignAdviser(sec.Section_ID, $event.target.value)" class="text-xs border-indigo-200 rounded bg-white text-indigo-700 cursor-pointer focus:ring-indigo-500 max-w-[120px]">
                      <option value="">No Adviser</option>
                      <option v-for="adv in availableAdvisers" :key="adv.Employee_ID" :value="adv.Employee_ID">{{ adv.Lastname }}, {{ adv.Firstname }}</option>
                    </select>
                  </div>
                </li>
              </ul>
            </div>
            <div class="bg-white shadow-sm rounded-xl border border-gray-200 p-6 hover:shadow-md transition-shadow duration-300">
              <div class="flex justify-between items-center mb-4">
                <h3 class="text-xl font-bold text-gray-900">Subjects</h3>
                <select v-model="subjectFilter" class="border border-gray-300 rounded text-sm p-1 text-gray-700 font-medium bg-gray-50 hover:bg-gray-100 cursor-pointer outline-none focus:ring-blue-500">
                  <option value="ALL">All</option><option value="11">Gr. 11</option><option value="12">Gr. 12</option>
                </select>
              </div>
              <form @submit.prevent="saveSubject" class="space-y-3 mb-6">
                <div class="flex space-x-2">
                  <input v-model="subjectForm.subject_code" type="text" placeholder="Code (e.g. PE1)" required class="w-1/3 border border-gray-300 rounded p-2 text-sm focus:ring-blue-500 transition-all" />
                  <select v-model.number="subjectForm.level_id" class="w-1/3 border border-gray-300 rounded p-2 text-sm focus:ring-blue-500 transition-all">
                    <option value="11">Gr. 11</option><option value="12">Gr. 12</option>
                  </select>
                  <select v-model="subjectForm.subject_type" class="w-1/3 border border-gray-300 rounded p-2 text-sm focus:ring-blue-500 transition-all bg-blue-50">
                    <option value="Core">Core</option><option value="Applied">Applied</option><option value="Specialized">Specialized</option>
                  </select>
                </div>
                <div class="flex space-x-2">
                  <input v-model="subjectForm.subject_name" type="text" placeholder="Full Name" required class="flex-1 border border-gray-300 rounded p-2 text-sm focus:ring-blue-500 transition-all" />
                  <select v-if="subjectForm.subject_type === 'Specialized'" v-model.number="subjectForm.strand_id" required class="w-1/3 border border-green-300 rounded p-2 text-sm focus:ring-green-500 transition-all bg-green-50 text-green-800">
                    <option value="" disabled>Select Strand...</option>
                    <option v-for="str in strands" :key="str.Strand_ID" :value="str.Strand_ID">{{ str.Strand_Code }}</option>
                  </select>
                </div>
                <button type="submit" class="w-full bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition-all shadow-sm">Add Subject</button>
              </form>
              <ul class="divide-y divide-gray-200 max-h-96 overflow-y-auto">
                <li v-for="sub in filteredAndSortedSubjects" :key="sub.Subject_Code" class="py-3 flex justify-between items-center hover:bg-gray-50 px-2 rounded transition-colors">
                  <div>
                    <p class="font-bold text-sm text-gray-900">
                      {{ sub.Subject_Code }} 
                      <span class="text-xs font-semibold px-2 py-0.5 rounded-full ml-2" :class="sub.Level_ID === 11 ? 'bg-indigo-100 text-indigo-800' : 'bg-purple-100 text-purple-800'">Gr. {{ sub.Level_ID }}</span>
                      <span v-if="sub.Subject_Type === 'Specialized' && sub.Strand_ID" class="text-xs font-bold px-2 py-0.5 rounded-full ml-1 bg-green-100 text-green-800">{{ strands.find(s => s.Strand_ID === sub.Strand_ID)?.Strand_Code || 'Specialized' }}</span>
                      <span v-else-if="sub.Subject_Type === 'Applied'" class="text-xs font-bold px-2 py-0.5 rounded-full ml-1 bg-yellow-100 text-yellow-800">Applied</span>
                      <span v-else class="text-xs font-bold px-2 py-0.5 rounded-full ml-1 bg-gray-100 text-gray-600">Core</span>
                    </p>
                    <p class="text-xs text-gray-600 mt-1">{{ sub.Subject_Name }}</p>
                  </div>
                  <div class="flex space-x-3 items-center ml-2">
                    <button @click="editSubject(sub)" class="text-blue-500 hover:text-blue-700 text-xs font-bold transition-colors">Edit</button>
                    <button @click="deleteSubject(sub.Subject_Code)" class="text-red-500 hover:text-red-700 text-xs font-bold transition-colors">Del</button>
                  </div>
                </li>
              </ul>
            </div>

          </div>

        </div>
      </transition>
    </div>

    <div v-if="showProfileModal" class="fixed inset-0 bg-slate-500/20 backdrop-blur-md flex items-center justify-center p-4 z-50 transition-opacity">
      <div class="bg-white rounded-xl shadow-2xl max-w-md w-full p-6 transform transition-transform">
        <h3 class="text-lg font-bold text-gray-900 mb-4">My Profile Settings</h3>
        <form @submit.prevent="updatePrincipalProfile" class="space-y-4">
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700">First Name</label>
              <input v-model="profileForm.firstname" type="text" required class="mt-1 block w-full border border-gray-300 rounded-md p-2 focus:ring-blue-500 transition-all" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700">Last Name</label>
              <input v-model="profileForm.lastname" type="text" required class="mt-1 block w-full border border-gray-300 rounded-md p-2 focus:ring-blue-500 transition-all" />
            </div>
          </div>
          
          <div class="mt-4">
            <label class="block text-sm font-medium text-gray-700">Middle Name (Optional)</label>
            <input v-model="profileForm.middlename" type="text" class="mt-1 block w-full border border-gray-300 rounded-md p-2 focus:ring-blue-500 transition-all" />
          </div>
          
          <div class="grid grid-cols-2 gap-4 mt-4">
            <div>
              <label class="block text-sm font-medium text-gray-700">Birth Date</label>
              <input v-model="profileForm.birth_date" type="date" class="mt-1 block w-full border border-gray-300 rounded-md p-2 focus:ring-blue-500 transition-all" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700">Sex</label>
              <select v-model="profileForm.sex" required class="mt-1 block w-full border border-gray-300 rounded-md p-2 focus:ring-blue-500 transition-all">
                <option value="M">Male</option>
                <option value="F">Female</option>
              </select>
            </div>
          </div>
          
          <hr class="my-4 border-gray-200" />
          
          <h4 class="text-sm font-bold text-gray-600 uppercase tracking-wide">Change Password (Optional)</h4>
          <div>
            <label class="block text-sm font-medium text-gray-700">Current Password</label>
            <div class="relative">
              <input v-model="profileForm.old_password" :type="showOldPassword ? 'text' : 'password'" placeholder="Leave blank to keep current" class="mt-1 block w-full border border-gray-300 rounded-md p-2 pr-10 focus:ring-blue-500 transition-all" />
              <button type="button" @click="showOldPassword = !showOldPassword" class="absolute inset-y-0 right-0 pr-3 flex items-center text-gray-400 hover:text-gray-600 focus:outline-none mt-1">
                <svg v-if="!showOldPassword" class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" /><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" /></svg>
                <svg v-else class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21" /></svg>
              </button>
            </div>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700">New Password</label>
            <div class="relative">
              <input v-model="profileForm.new_password" :type="showNewPassword ? 'text' : 'password'" placeholder="Enter new password" class="mt-1 block w-full border border-gray-300 rounded-md p-2 pr-10 focus:ring-blue-500 transition-all" />
              <button type="button" @click="showNewPassword = !showNewPassword" class="absolute inset-y-0 right-0 pr-3 flex items-center text-gray-400 hover:text-gray-600 focus:outline-none mt-1">
                <svg v-if="!showNewPassword" class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" /><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" /></svg>
                <svg v-else class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21" /></svg>
              </button>
            </div>
          </div>
          <div class="mt-6 flex justify-end space-x-3">
            <button type="button" @click="showProfileModal = false" class="px-4 py-2 border border-gray-300 text-gray-700 hover:bg-gray-50 rounded-md transition-colors">Cancel</button>
            <button type="submit" class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 hover:-translate-y-0.5 shadow-sm transition-all">Save Changes</button>
          </div>
        </form>
      </div>
    </div>

    <div v-if="showViewGradesModal" class="fixed inset-0 bg-slate-500/20 backdrop-blur-md flex items-center justify-center p-4 z-50 transition-opacity">
      <div class="bg-white rounded-lg shadow-xl max-w-2xl w-full p-6 max-h-[90vh] flex flex-col">
        <div class="flex justify-between items-center mb-4">
          <h3 class="text-lg font-bold text-gray-900">Batch #{{ selectedBatchId }} Details</h3>
          <button @click="showViewGradesModal = false" class="text-gray-500 hover:text-gray-700 text-2xl">&times;</button>
        </div>
        <div class="overflow-y-auto flex-1 border rounded-md">
          <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50 sticky top-0">
              <tr>
                <th class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">LRN</th>
                <th class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">Name</th>
                <th class="px-4 py-2 text-center text-xs font-medium text-gray-500 uppercase">Q1</th>
                <th class="px-4 py-2 text-center text-xs font-medium text-gray-500 uppercase">Q2</th>
                <th class="px-4 py-2 text-center text-xs font-bold text-blue-600 uppercase">Final</th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <tr v-for="grade in currentBatchGrades" :key="grade.LRN">
                <td class="px-4 py-2 text-sm text-gray-900">{{ grade.LRN }}</td>
                <td class="px-4 py-2 text-sm text-gray-700">{{ grade.Name }}</td>
                <td class="px-4 py-2 text-sm text-center">{{ grade.Q1 }}</td>
                <td class="px-4 py-2 text-sm text-center">{{ grade.Q2 }}</td>
                <td class="px-4 py-2 text-sm text-center font-bold text-blue-600">{{ grade.Final }}</td>
              </tr>
            </tbody>
          </table>
        </div>
        <div class="mt-4 flex justify-end">
          <button @click="showViewGradesModal = false" class="px-4 py-2 bg-gray-200 text-gray-800 rounded-md hover:bg-gray-300">Close</button>
        </div>
      </div>
    </div>

    <div v-if="showTeacherModal" class="fixed inset-0 bg-slate-500/20 backdrop-blur-md flex items-center justify-center p-4 z-50 transition-opacity">
      <div class="bg-white rounded-lg shadow-xl max-w-md w-full p-6">
        <h3 class="text-lg font-bold text-gray-900 mb-4">{{ isEditingTeacher ? 'Edit Teacher' : 'Add New Teacher' }}</h3>
        <form @submit.prevent="saveTeacher">
            <div class="mb-4">
              <label class="block text-sm font-medium text-gray-700 mb-1">Employee ID</label>
              <input v-model="teacherForm.employee_id" type="text" required :disabled="isEditingTeacher" class="w-full border border-gray-300 rounded p-2 text-sm focus:ring-blue-500 disabled:bg-gray-100" />
            </div>
            <div class="mb-4">
              <label class="block text-sm font-medium text-gray-700 mb-1">Last Name</label>
              <input v-model="teacherForm.lastname" type="text" required class="w-full border border-gray-300 rounded p-2 text-sm focus:ring-blue-500" />
            </div>
            <div class="mb-4">
              <label class="block text-sm font-medium text-gray-700 mb-1">First Name</label>
              <input v-model="teacherForm.firstname" type="text" required class="w-full border border-gray-300 rounded p-2 text-sm focus:ring-blue-500" />
            </div>
            <div class="mb-4">
              <label class="block text-sm font-medium text-gray-700 mb-1">Middle Name (Optional)</label>
              <input v-model="teacherForm.middlename" type="text" class="w-full border border-gray-300 rounded p-2 text-sm focus:ring-blue-500" />
            </div>
            <div class="flex space-x-4 mb-4">
              <div class="flex-1">
                <label class="block text-sm font-medium text-gray-700 mb-1">Birth Date</label>
                <input v-model="teacherForm.birth_date" type="date" class="w-full border border-gray-300 rounded p-2 text-sm focus:ring-blue-500" />
              </div>
              <div class="w-1/3">
                <label class="block text-sm font-medium text-gray-700 mb-1">Sex</label>
                <select v-model="teacherForm.sex" required class="w-full border border-gray-300 rounded p-2 text-sm focus:ring-blue-500">
                  <option value="M">Male</option>
                  <option value="F">Female</option>
                </select>
              </div>
            </div>
            <div class="mb-4">
              <label class="block text-sm font-medium text-gray-700 mb-1">Role</label>
              <select v-model="teacherForm.role" required class="w-full border border-gray-300 rounded p-2 text-sm focus:ring-blue-500">
                <option value="Subject Teacher">Subject Teacher</option>
                <option value="Adviser">Adviser</option>
              </select>
            </div>
            <div v-if="!isEditingTeacher">
              <p class="text-xs text-gray-500 mt-2">Default password for new teachers is <strong>password123</strong></p>
            </div>
            <div class="mt-6 flex justify-end space-x-3">
              <button type="button" @click="showTeacherModal = false" class="px-4 py-2 border border-gray-300 rounded text-gray-700 hover:bg-gray-50 transition-colors text-sm font-medium">Cancel</button>
              <button type="submit" class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition-colors shadow-sm text-sm font-medium">{{ isEditingTeacher ? 'Update Teacher' : 'Save Teacher' }}</button>
            </div>
          </form>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, reactive, onMounted, onUnmounted, computed } from 'vue';
import { useRouter } from 'vue-router';
import api from '../api';
import { logout as performLogout } from '../auth';

const router = useRouter();
const activeTab = ref('overview'); 
const principalId = localStorage.getItem('employee_id');

const principalName = ref('');
const showProfileModal = ref(false);
const profileForm = reactive({ firstname: '', lastname: '', middlename: '', birth_date: '', sex: 'M', old_password: '', new_password: '' });
const showOldPassword = ref(false);
const showNewPassword = ref(false);

const stats = ref({
  teachers: 0, students: { total: 0, g11: 0, g12: 0 }, sections: 0,
  submissions: { total: 0, approved: 0, pending: 0, rate: 0 }
});
const studentStatFilter = ref('ALL');

const displayedStudentCount = computed(() => {
  if (!stats.value.students) return 0;
  if (studentStatFilter.value === '11') return stats.value.students.g11;
  if (studentStatFilter.value === '12') return stats.value.students.g12;
  return stats.value.students.total;
});

const submissions = ref([]);
const approvalFilter = ref('Pending');
const filteredSubmissions = computed(() => {
  return submissions.value.filter(s => s.Status === approvalFilter.value);
});
const showViewGradesModal = ref(false);
const currentBatchGrades = ref([]);
const selectedBatchId = ref(null);

const teachers = ref([]);
const showTeacherModal = ref(false);
const isEditingTeacher = ref(false);
const teacherForm = reactive({ employee_id: '', firstname: '', lastname: '', middlename: '', birth_date: '', sex: 'M', role: 'Subject Teacher' });

// Maps Advisers cleanly
const availableAdvisers = computed(() => {
  return teachers.value.filter(t => t.Teacher_Type === 'Adviser' || t.Teacher_Type === 'Class Adviser');
});

// --- RESTORED CURRICULUM & TERM STATE ---
const activeTerm = reactive({ school_year: '', semester: '1st' });

const strands = ref([]);
const strandForm = reactive({ track_name: '', strand_code: '', strand_name: '' });

const sections = ref([]);
const sectionFilter = ref('ALL');
const sectionForm = reactive({ section_name: '', level_id: 11, strand_id: '', adviser_id: '' });

const filteredAndSortedSections = computed(() => {
  if (!sections.value) return [];
  let filtered = sections.value;
  if (sectionFilter.value !== 'ALL') {
    filtered = filtered.filter(s => s.Level_ID == sectionFilter.value);
  }
  return filtered;
});

const subjects = ref([]);
const subjectFilter = ref('ALL');
const isEditingSubject = ref(false);
const editingSubjectCode = ref(null);
const subjectForm = reactive({ subject_code: '', subject_name: '', level_id: 11, subject_type: 'Core', strand_id: '' });

const filteredAndSortedSubjects = computed(() => {
  if (!subjects.value) return [];
  let filtered = subjects.value;
  if (subjectFilter.value !== 'ALL') {
    filtered = filtered.filter(s => s.Level_ID == subjectFilter.value);
  }
  return filtered;
});

const assignAdviser = async (sectionId, adviserId) => {
  try {
    await api.put(`/api/principal/sections/${sectionId}/assign-adviser`, { adviser_id: adviserId || null });
    fetchCurriculum(); 
  } catch (error) {
    alert(error.response?.data?.detail || error.message); 
    fetchCurriculum(); 
  }
};

// --- PRINCIPAL PROFILE LOGIC ---
const fetchPrincipalProfile = async () => {
  try {
    const res = await api.get(`/api/principal/${principalId}/profile`);
    const data = res.data;
    principalName.value = data.name;
    profileForm.firstname = data.firstname;
    profileForm.lastname = data.lastname;
    profileForm.middlename = data.middlename || '';
    profileForm.birth_date = data.birth_date || '';
    profileForm.sex = data.sex || 'M';
  } catch (e) { console.error(e); }
};

const updatePrincipalProfile = async () => {
  try {
    const payload = { ...profileForm };
    // Safety check: Convert empty strings to null so backend doesn't crash!
    if (!payload.birth_date) payload.birth_date = null;
    if (!payload.middlename) payload.middlename = null;
    if (!payload.old_password) payload.old_password = null;
    if (!payload.new_password) payload.new_password = null;

    await api.put(`/api/principal/${principalId}/profile`, payload);
    
    alert("Profile updated successfully!");
    showProfileModal.value = false;
    profileForm.old_password = ''; profileForm.new_password = '';
    fetchPrincipalProfile();
  } catch (error) { 
    alert("Error:\n" + (error.response?.data?.detail || error.message)); 
  }
};

const fetchStats = async () => {
  try {
    const res = await api.get('/api/principal/stats');
    stats.value = res.data;
  } catch (error) { console.error(error); }
};

const fetchSubmissions = async () => {
  try {
    const response = await api.get('/api/principal/submissions');
    submissions.value = response.data;
  } catch (error) { console.error(error); }
};

const viewGrades = async (submissionId) => {
  selectedBatchId.value = submissionId;
  try {
    const response = await api.get(`/api/principal/submissions/${submissionId}/grades`);
    currentBatchGrades.value = response.data;
    showViewGradesModal.value = true;
  } catch (error) { console.error(error); }
};

const approveBatch = async (submissionId) => {
  if (confirm(`Approve Batch #${submissionId}?`)) {
    try {
      await api.post('/api/principal/approve', { submission_id: submissionId, principal_id: principalId });
      fetchSubmissions(); fetchStats(); 
    } catch (error) { alert(error.response?.data?.detail || error.message); }
  }
};

const rejectBatch = async (submissionId) => {
  if (confirm(`Return Batch #${submissionId} to the teacher?`)) {
    try {
      await api.post('/api/principal/reject', { submission_id: submissionId, principal_id: principalId });
      fetchSubmissions(); fetchStats();
    } catch (error) { alert(error.response?.data?.detail || error.message); }
  }
};

const deleteSubmission = async (submissionId) => {
  if (confirm(`WARNING: Are you sure you want to permanently delete Submission #${submissionId}? This will wipe all its grade records.`)) {
    try {
      await api.delete(`/api/principal/submissions/${submissionId}`);
      fetchSubmissions(); fetchStats();
    } catch (error) { alert(error.response?.data?.detail || "Error deleting submission"); }
  }
};

const exportGrades = async (submissionId) => {
  try {
    const res = await api.get(`/api/principal/submissions/${submissionId}/export`, { responseType: 'blob' });
    const url = window.URL.createObjectURL(new Blob([res.data]));
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', `Batch_${submissionId}_Grades.csv`);
    document.body.appendChild(link);
    link.click();
    link.remove();
  } catch(e) {
    alert("Failed to export grades.");
  }
};

// --- TEACHER LOGIC ---
const fetchTeachers = async () => {
  try {
    const response = await api.get('/api/principal/teachers');
    teachers.value = response.data;
  } catch (error) { console.error(error); }
};

const openTeacherModal = (teacher = null) => {
  if (teacher && teacher.Employee_ID) {
    isEditingTeacher.value = true;
    teacherForm.employee_id = teacher.Employee_ID || '';
    teacherForm.firstname = teacher.Firstname || '';
    teacherForm.lastname = teacher.Lastname || '';
    teacherForm.middlename = teacher.Middlename || '';
    teacherForm.birth_date = teacher.Birth_Date || '';
    teacherForm.sex = teacher.Sex || 'M';
    
    let dbRole = teacher.Teacher_Type || 'Subject Teacher';
    if (dbRole === 'Class Adviser') dbRole = 'Adviser';
    teacherForm.role = dbRole; 
  } else {
    isEditingTeacher.value = false;
    teacherForm.employee_id = '';
    teacherForm.firstname = '';
    teacherForm.lastname = '';
    teacherForm.middlename = '';
    teacherForm.birth_date = '';
    teacherForm.sex = 'M';
    teacherForm.role = 'Subject Teacher';
  }
  showTeacherModal.value = true;
};

const saveTeacher = async () => {
  try {
    // Safety check: Convert empty strings to null
    const payload = { ...teacherForm };
    if (!payload.birth_date) payload.birth_date = null;
    if (!payload.middlename) payload.middlename = null;

    if (isEditingTeacher.value) {
      await api.put(`/api/principal/teachers/${teacherForm.employee_id}`, payload);
    } else {
      await api.post('/api/principal/teachers', payload);
    }
    
    showTeacherModal.value = false;
    fetchTeachers(); fetchStats();
  } catch (error) { 
    alert("Operation failed:\n" + (error.response?.data?.detail || error.message)); 
  }
};

const deleteTeacher = async (id) => {
  if (confirm(`Remove teacher ${id}?`)) {
    try {
      await api.delete(`/api/principal/teachers/${id}`);
      fetchTeachers(); fetchStats();
    } catch (error) { alert(error.response?.data?.detail || error.message); }
  }
};

// --- CURRICULUM METHODS ---
const fetchCurriculum = async () => {
  try {
    const [subRes, secRes, strRes] = await Promise.all([
      api.get('/api/curriculum/subjects'), 
      api.get('/api/principal/sections'),
      api.get('/api/curriculum/strands')
    ]);
    subjects.value = subRes.data;
    sections.value = secRes.data;
    strands.value = strRes.data;
  } catch (e) { console.error(e); }
};

const saveStrand = async () => {
  try {
    await api.post('/api/principal/strands', strandForm);
    strandForm.strand_code = ''; strandForm.strand_name = ''; 
    fetchCurriculum();
  } catch (e) { 
      alert("Error: " + (e.response?.data?.detail || e.message)); 
  }
};

const deleteStrand = async (id) => {
  if (confirm(`Delete Strand? Make sure no sections are currently using it!`)) {
    try {
      await api.delete(`/api/principal/strands/${id}`);
      fetchCurriculum();
    } catch (e) { alert(e.response?.data?.detail || e.message); }
  }
};

const editSubject = (sub) => {
  isEditingSubject.value = true;
  editingSubjectCode.value = sub.Subject_Code;
  subjectForm.subject_code = sub.Subject_Code;
  subjectForm.subject_name = sub.Subject_Name;
  subjectForm.level_id = sub.Level_ID;
  subjectForm.subject_type = sub.Subject_Type || 'Core';
  subjectForm.strand_id = sub.Strand_ID || '';
};

const cancelEditSubject = () => {
  isEditingSubject.value = false;
  editingSubjectCode.value = null;
  subjectForm.subject_code = ''; 
  subjectForm.subject_name = '';
  subjectForm.subject_type = 'Core';
  subjectForm.strand_id = '';
};

const saveSubject = async () => {
  try {
    const payload = {
      subject_code: subjectForm.subject_code,
      subject_name: subjectForm.subject_name,
      level_id: subjectForm.level_id,
      subject_type: subjectForm.subject_type,
      strand_id: (subjectForm.subject_type === 'Specialized' && subjectForm.strand_id !== '') ? subjectForm.strand_id : null
    };

    if (isEditingSubject.value) {
      await api.put(`/api/principal/subjects/${editingSubjectCode.value}`, payload);
    } else {
      await api.post('/api/principal/subjects', payload);
    }

    cancelEditSubject(); // Reset the form completely
    fetchCurriculum();   // Refresh the list
  } catch (e) { 
    alert("Error Details:\n" + (e.response?.data?.detail || e.message)); 
  }
};

const deleteSubject = async (code) => {
  if (confirm(`Delete Subject ${code}?`)) {
    try {
      await api.delete(`/api/principal/subjects/${code}`);
      fetchCurriculum();
    } catch (e) { alert(e.response?.data?.detail || e.message); }
  }
};

const saveSection = async () => {
  try {
    await api.post('/api/principal/sections', sectionForm);
    sectionForm.section_name = ''; sectionForm.strand_id = '';
    fetchCurriculum(); fetchStats();
  } catch (e) { 
    alert(e.response?.data?.detail || "Section Name already exists!"); 
  }
};

const deleteSection = async (id) => {
  if (confirm(`Delete Section ID ${id}?`)) {
    try {
      await api.delete(`/api/principal/sections/${id}`);
      fetchCurriculum(); fetchStats();
    } catch (e) { alert(e.response?.data?.detail || e.message); }
  }
};

const logout = () => { performLogout(); };

// --- SYSTEM TERM API FUNCTIONS ---
const fetchActiveTerm = async () => {
  try {
    const res = await api.get('/api/settings/term');
    activeTerm.school_year = res.data.school_year;
    activeTerm.semester = res.data.semester;
  } catch (error) {
    console.error("Failed to fetch active term:", error);
  }
};

const saveActiveTerm = async () => {
  try {
    await api.post('/api/settings/term', { 
      school_year: activeTerm.school_year, 
      semester: activeTerm.semester 
    });
    alert(`Success! The entire system is now operating in the ${activeTerm.semester} Semester of ${activeTerm.school_year}.`);
  } catch (error) {
    alert(error.response?.data?.detail || error.message);
  }
};

const archiveSchoolYear = async () => {
  if (confirm("WARNING: This will archive all current student sections and advance the school year. Students will need to be re-enrolled into new sections. Proceed?")) {
    try {
      const res = await api.post('/api/principal/archive-school-year');
      alert(res.data.message);
      fetchActiveTerm();
      fetchStats();
    } catch (error) {
      alert("Error: " + (error.response?.data?.detail || error.message));
    }
  }
};

let pollInterval;
onMounted(() => {
  fetchPrincipalProfile(); 
  fetchStats(); fetchSubmissions(); fetchTeachers(); fetchCurriculum(); fetchActiveTerm();
  pollInterval = setInterval(() => {
    fetchStats();
    fetchSubmissions();
  }, 3000);
});
onUnmounted(() => clearInterval(pollInterval));
</script>

<style scoped>
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
</style>