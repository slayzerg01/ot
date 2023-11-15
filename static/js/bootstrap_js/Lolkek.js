let numbers = [1, 2 , 5, 11 , 15];
let reverse = numbers.length - 1;

for (let i = 0; i < numbers.length / 2; i++) {
    let swap = numbers[reverse];
    numbers[reverse] = numbers[i];
    numbers[i] = swap;
    reverse--;
}

console.log(numbers);
  
  /*
  
  Создайте функцию getZippedArrays.
  
  У функции должно быть два параметра. Первый — массив с названиями ключей. Второй — массив со значениями этих ключей.
  
  Функция должна собирать из этих двух массивов объект и возвращать его. Каждому элементу из массива ключей соответствует элемент из массива значений.
  
  */
  