import {Modal, Result, Button} from "antd";


function ResultModal({isOpen, onClose, isOk, patient}) {
    return (
        <Modal open={isOpen} onCancel={onClose} footer={<Button variant={'outlined'} color={'cyan'} onClick={onClose}>Закрыть</Button>}>
            {isOk ? (<Result status={"success"} title={'ИБ успешно добавлена'} subTitle={`Пациент: ${patient.fio}. Номер ИБ: ${patient.ib_num}`} />) :
                <Result status={"error"} title={'Что-то пошло не так'} subTitle={"Проверьте правльно ли все подключенно и попробуйте еще раз"}/>}

        </Modal>
    )
}

export default ResultModal