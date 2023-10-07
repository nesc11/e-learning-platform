const getModulesOrder = modules => {
    return modules.map((item, index) => {
        return {
            id: item.dataset.id,
            order: index
        }
    })
}

const checkOrderChanges = (order, newOrder) => {
    let changes = []
    order.forEach((orderItem, index) => {
        if (orderItem.id !== newOrder[index].id) {
            changes.push(newOrder[index])
        }
    })
    return changes
}

async function postOrderChanges(url, data) {
    try {
        const response = await fetch(url, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(data),
        })

        // const result = await response.json();
        // console.log("Success:", result);
    } catch (error) {
        console.error("Error:", error);
    }
}

document.addEventListener('DOMContentLoaded', e => {
    const modules = document.getElementById('modules')
    const moduleItemEls = document.querySelectorAll('.module-item-el')

    let order = getModulesOrder([...moduleItemEls])
    console.log(order)

    if (moduleItemEls.length > 0) {
        moduleItemEls.forEach(item => {
            item.addEventListener('dragstart', e => {
                e.currentTarget.classList.add('dragging')
            })
            item.addEventListener('dragend', e => {
                e.currentTarget.classList.remove('dragging')
                let newOrder = getModulesOrder([...document.querySelectorAll('.module-item-el')])
                let changes = checkOrderChanges(order, newOrder)
                if (changes.length > 0) {
                    console.log(changes)
                    order = [...newOrder]
                    postOrderChanges('/course/modules/order/', changes)
                }
            })
        })
    }

    if (modules) {
        modules.addEventListener('dragover', e => {
            e.preventDefault()
            const draggable = e.currentTarget.querySelector('.dragging')
            const moduleSiblings = [...modules.querySelectorAll('.module-item-el:not(.dragging)')]
            const nextSibling = moduleSiblings.find(sibling => {
                return e.clientY <= sibling.offsetTop + sibling.offsetHeight / 2
            })
            // console.log(nextSibling)
            e.currentTarget.insertBefore(draggable, nextSibling)

        })
    }
})
