let swaps = [];

function swap(arr,a,b){
    let temp = arr[a];
    arr[a] = arr[b];
    arr[b] = temp;
}

function parent(index){
    return Math.floor((index -1)/2);
}

function leftChild(index){
    return 2* index + 1;
}
function rightChild(index){
    return 2* index + 2;
}

function makeHeap(arr){
    let i;//index of next element to be added to the heap
    let k;//index of new element as it is being pushed
    for(i = 1;i<arr.length;++i){
        k = i;
        while(k>0 && arr[k] >arr[parent(k)]){
            swap(arr,parent(k),k);
            k = parent(k);
        }
    }
    return arr;
}


function reheapifyDown(arr,length){
    let index = 0;
    let bigChildIndex;
    let isHeap = false;
    //loop keeps going while the array is not a heap and the current element has at least
    // a left child. If the leftChild(index) is greater than the length of the array, the index
    // does not have any children
    while(!isHeap && leftChild(index)<length){
        if(rightChild(index) >= length){// no right child
            bigChildIndex= leftChild(index);
        }
        else if(arr[leftChild(index)] > arr[rightChild(index)]){
            bigChildIndex  = leftChild(index);
        }
        else{
            bigChildIndex = rightChild(index);
        }

        if( arr[index] < arr[bigChildIndex]){
            swaps.push([index,bigChildIndex]);
            console.log('reheapifying',index,bigChildIndex);
            swap(arr,index,bigChildIndex)
            index = bigChildIndex;
        }
        else {
            isHeap = true;
        }
    }
}
