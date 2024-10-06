// const div_question_number = document.getElementById('question-number')
// const div_question_text = document.getElementById('question-text')

// const rad_option1 = document.getElementById('option1')
// const rad_option2 = document.getElementById('option2')
// const rad_option3 = document.getElementById('option3')
// const rad_option4 = document.getElementById('option4')

// const lbl_option1 = document.getElementById('lbl-option1')
// const lbl_option2 = document.getElementById('lbl-option2')
// const lbl_option3 = document.getElementById('lbl-option3')
// const lbl_option4 = document.getElementById('lbl-option4')

// const user = user_data
// const subject = subject_data

// let current_question = null
// let current_question_id = null
// let current_user_answer = null

// let cummulative_score = 0
// let question_counter = 0
// let total_score = 0
// let previous_questions = []

// let all_questions_answered = []
// let current_question_number = 0

// const MARKS = 5

// // alert(`User: ${user.fullname}`)
// // alert(`Subject: ${subject.id}`)

// // starts quiz and fetch first question
// async function startQuiz(){
//     document.getElementById("quiz-question-wrapper").style.display = 'block'
//     document.getElementById("btn-show-quiz").style.display = 'None'

//     await fetchQuestion()
// }

// // submit current answer and fetch next question
// const next_question = async (e) => {
//     e.preventDefault()

//     if(rad_option1.checked || rad_option2.checked || rad_option3.checked || rad_option4.checked) {
//         if(rad_option1.checked){
//             current_user_answer = rad_option1.value
//         } else if(rad_option2.checked){
//             current_user_answer = rad_option2.value
//         } else if(rad_option3.checked){
//             current_user_answer = rad_option3.value
//         } else if(rad_option4.checked){
//             current_user_answer = rad_option4.value
//         } 

//         if(current_user_answer === current_question.answer){
//             total_score += MARKS
//         }
    
//         current_question_number++
//         previous_questions.push(current_question.id)
        
//         const question_records = { 
//             ...current_question, 
//             user_answer: current_user_answer, 
//             number:current_question_number 
//         }
        
//         all_questions_answered.push(question_records)
        
//         console.log('All Answered: ', all_questions_answered)
//         // await fetchQuestion()
            
//     } else{
        
//         alert('Sorry you need to select an answer first.')
//     }
    
// }

// const submitResults = async (e) => {
//     e.preventDefault()

//     // TO-DO: submit results
//     const overall_marks = len(all_questions_answered) * MARKS
//     alert(`${user.fullname}, your score in ${subject.name} is ${total_score} out of ${overall_marks} marks`)

//     resetVariables()

//     return
// }

// const fetchQuestion = async () => {
//     const data = { previous_questions }

//     try {
//         const response = await fetch(`/subjects/${subject.id}/next_question`, {
//             method: 'POST',
//             headers: {
//                 'Content-Type': 'application/json',
//                 'Accept': 'application/json',
//             },
//             body: JSON.stringify(data)
//         })
    
//         const results = await response.json()
    
//         // console.log(results)
//         if(results.success){
//             current_question = results.question
//             current_question_id = current_question.id
//             question_counter++

//             displayQuestion(current_question, question_counter)
//         } else if(!results.success && results?.end){ // end of questions
//             if(confirm('End of questions, Submit quiz now?')){
//                 await submitResults()
//             }

//             return
//         }

//     } catch (error) {
//         console.log('Error: ', error)
//     }
// }



// const displayQuestion = (fetched_question, question_number) => {
//     if(fetched_question){
//         rad_option1.checked = false
//         rad_option2.checked = false
//         rad_option3.checked = false
//         rad_option4.checked = false

//         div_question_number.innerText = `Question ${question_number}`
//         div_question_text.innerText = fetched_question.question

//         // Shuffle options
//         // const question = fetched_question.question
//         const options = [fetched_question.answer, fetched_question.option1, fetched_question.option2, fetched_question.option3]
        
//         const shuffled_options = shuffleOptions(options)

//         // Display options in random order
//         rad_option1.value = shuffled_options[0]
//         lbl_option1.innerText = shuffled_options[0]

//         rad_option2.value = shuffled_options[1]
//         lbl_option2.innerText = shuffled_options[1]
        
//         rad_option3.value = shuffled_options[2]
//         lbl_option3.innerText = shuffled_options[2]
        
//         rad_option4.value = shuffled_options[3]
//         lbl_option4.innerText = shuffled_options[3]
//     }
// }

// function shuffleOptions(array) {
//     return array.sort(() => Math.random() - 0.5);
// }

// const resetVariables = () => {
//     current_question = null
//     current_question_id = null
//     current_user_answer = null

//     cummulative_score = 0
//     question_counter = 0
//     total_score = 0
//     previous_questions = []

//     all_questions_answered = []
//     current_question_number = 0
// }