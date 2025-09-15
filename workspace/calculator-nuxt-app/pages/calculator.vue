<template>
  <div class="calculator">
    <div class="display-container">
      <input :value="display" readonly class="display"/>
    </div>
    <div class="buttons">
      <!-- Row 1: Clear and operators -->
      <button class="btn-clear" @click="clearAll">C</button>
      <button class="btn-operator" @click="inputOperator('/')">/</button>
      <button class="btn-operator" @click="inputOperator('*')">×</button>
      <button class="btn-operator" @click="inputOperator('-')">−</button>
      
      <!-- Row 2: 7, 8, 9, + -->
      <button class="btn-number" @click="inputDigit('7')">7</button>
      <button class="btn-number" @click="inputDigit('8')">8</button>
      <button class="btn-number" @click="inputDigit('9')">9</button>
      <button class="btn-operator btn-plus" @click="inputOperator('+')">+</button>
      
      <!-- Row 3: 4, 5, 6 -->
      <button class="btn-number" @click="inputDigit('4')">4</button>
      <button class="btn-number" @click="inputDigit('5')">5</button>
      <button class="btn-number" @click="inputDigit('6')">6</button>
      
      <!-- Row 4: 1, 2, 3, = -->
      <button class="btn-number" @click="inputDigit('1')">1</button>
      <button class="btn-number" @click="inputDigit('2')">2</button>
      <button class="btn-number" @click="inputDigit('3')">3</button>
      <button class="btn-equals" @click="equals">=</button>
      
      <!-- Row 5: 0, . -->
      <button class="btn-number btn-zero" @click="inputDigit('0')">0</button>
      <button class="btn-number" @click="inputDigit('.')">.</button>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, computed } from 'vue';

type Operator = '+' | '-' | '*' | '/'

const current = ref<string>('')
const previous = ref<number | null>(null)
const operator = ref<Operator | null>(null)
const justEvaluated = ref<boolean>(false)
const hasError = ref<boolean>(false)

const display = computed(() => {
  if (hasError.value) return 'Error'
  if (current.value !== '') return current.value
  if (previous.value !== null) return formatNumber(previous.value)
  return '0'
})

function formatNumber(num: number): string {
  // Handle very large or very small numbers
  if (Math.abs(num) > 999999999 || (Math.abs(num) < 0.000001 && num !== 0)) {
    return num.toExponential(6)
  }
  
  // Remove trailing zeros for whole numbers
  if (num % 1 === 0) {
    return num.toString()
  }
  
  // Limit decimal places to avoid floating point precision issues
  return parseFloat(num.toFixed(10)).toString()
}

function calculate(a: number, b: number, op: Operator): number {
  switch (op) {
    case '+': return a + b
    case '-': return a - b
    case '*': return a * b
    case '/': 
      if (b === 0) {
        throw new Error('Division by zero')
      }
      return a / b
  }
}

function clearAll() {
  current.value = ''
  previous.value = null
  operator.value = null
  justEvaluated.value = false
  hasError.value = false
}

function inputDigit(digit: string) {
  // If there's an error, clear it and start fresh
  if (hasError.value) {
    clearAll()
  }
  
  if (justEvaluated.value && operator.value === null) {
    // Start a new calculation after equals
    previous.value = null
    current.value = ''
    justEvaluated.value = false
  }
  
  if (digit === '.') {
    // Prevent multiple decimal points
    if (current.value.includes('.')) return
    
    // If current is empty, start with '0.'
    if (current.value === '') {
      current.value = '0.'
    } else {
      current.value += '.'
    }
    return
  }
  
  // Prevent leading zeros (except for '0' itself)
  if (digit === '0' && current.value === '0') {
    return // Don't add more zeros
  }
  
  // If current is '0', replace it with the new digit
  if (current.value === '0') {
    current.value = digit
  } else {
    current.value += digit
  }
}

function inputOperator(op: Operator) {
  // If there's an error, don't allow new operations
  if (hasError.value) return
  
  justEvaluated.value = false
  
  if (current.value !== '') {
    const curr = parseFloat(current.value)
    
    if (previous.value === null) {
      previous.value = curr
    } else if (operator.value) {
      try {
        const res = calculate(previous.value, curr, operator.value)
        previous.value = res
      } catch (error) {
        hasError.value = true
        previous.value = null
        operator.value = null
        return
      }
    }
    current.value = ''
  }
  
  operator.value = op
}

function equals() {
  // If there's an error, don't allow equals
  if (hasError.value) return
  
  if (operator.value && current.value !== '' && previous.value !== null) {
    const curr = parseFloat(current.value)
    
    try {
      const res = calculate(previous.value, curr, operator.value)
      previous.value = res
      current.value = ''
      operator.value = null
      justEvaluated.value = true
    } catch (error) {
      hasError.value = true
      previous.value = null
      operator.value = null
      justEvaluated.value = true
    }
  }
}
</script>

<style scoped>
.calculator {
  width: 320px;
  margin: 50px auto;
  background: #1a1a1a;
  border-radius: 20px;
  padding: 20px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.display-container {
  margin-bottom: 20px;
}

.display {
  width: 100%;
  height: 60px;
  background: #000;
  color: #fff;
  border: none;
  border-radius: 10px;
  font-size: 24px;
  font-weight: 300;
  text-align: right;
  padding: 0 20px;
  box-sizing: border-box;
  outline: none;
  font-family: 'Courier New', monospace;
}

.buttons {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 12px;
}

button {
  height: 60px;
  border: none;
  border-radius: 12px;
  font-size: 20px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  outline: none;
  user-select: none;
}

button:active {
  transform: scale(0.95);
}

.btn-number {
  background: #333;
  color: #fff;
}

.btn-number:hover {
  background: #444;
}

.btn-operator {
  background: #ff9500;
  color: #fff;
}

.btn-operator:hover {
  background: #ffad33;
}

.btn-clear {
  background: #a6a6a6;
  color: #000;
}

.btn-clear:hover {
  background: #bfbfbf;
}

.btn-equals {
  background: #ff9500;
  color: #fff;
  grid-row: span 2;
}

.btn-equals:hover {
  background: #ffad33;
}

.btn-zero {
  grid-column: span 2;
}

.btn-plus {
  grid-row: span 2;
}

/* Responsive design */
@media (max-width: 480px) {
  .calculator {
    width: 280px;
    margin: 20px auto;
    padding: 15px;
  }
  
  button {
    height: 50px;
    font-size: 18px;
  }
  
  .display {
    height: 50px;
    font-size: 20px;
  }
}
</style>

