import {Divider, List} from 'antd';
import {Button} from 'antd';
import {ScanOutlined} from '@ant-design/icons';
import InfiniteScroll from 'react-infinite-scroll-component';
import ModalChooseScanner from "./ModalChooseScanner.jsx";
import {useState} from "react";
import {getScanners} from "../api/scanner_api.js";
import ResultModal from "./ResultModal.jsx";

function UserList({data, isLoading, onScroll, groupDoc}) {
    const HEIGHT = window.screen.height
    const [isModalOpen, openModal] = useState(false)
    const [scanners, setScanners] = useState([])
    const [isScannersLoading, setIsScannersLoading] = useState(false)
    const [patient, setPatient] = useState('')
    const [resultModal, setResultModal] = useState(false)
    const [isScanOk, setIsScanOk] = useState(false)

    const onModalClose = async (code) => {
        if (code === 200) {
            setIsScanOk(true)
        }
        setResultModal(true)


    }

    const getScannersData = async () => {
        setIsScannersLoading(true)
        let sc = await getScanners()
        setScanners(sc)
        setIsScannersLoading(false)
    }

    const onModalOpen = async (patientData) => {
        openModal(true)
        setPatient(patientData)
        if (!scanners.length) {
            getScannersData()
        }
    }

    return (
        <>
            <div id="scrollableDiv"
                 style={{
                     height: '80vh',

                     overflow: 'auto',
                     scrollbarWidth: 0

                 }}>
                <InfiniteScroll
                    dataLength={data.length}
                    next={onScroll}
                    hasMore={data.length < data.length + 1}
                    loader={null}
                    endMessage={<Divider plain>It is all, nothing more 🤐</Divider>}
                    scrollableTarget="scrollableDiv"
                >
                    <List id='scrollingList' dataSource={data} size={'default'} loading={isLoading}
                          renderItem={(item, index) => (
                              <List.Item>
                                  <List.Item.Meta title={item.fio} description={
                                      <>
                                          {item.ib_num}
                                          {item.pacs_uid && ` / ${item.pacs_uid}`}
                                      </>
                                  } ></List.Item.Meta>
                                  <div>
                                      <Button color={'cyan'} variant={"solid"}
                                              onClick={() => onModalOpen(item)}><ScanOutlined/></Button>
                                  </div>
                              </List.Item>
                          )}>

                    </List>
                    <ModalChooseScanner open={isModalOpen} onCloseScan={onModalClose} data={scanners} reloadScanners={getScannersData} isLoading={isScannersLoading} groupDoc={groupDoc} patient={patient} onClose={() => {openModal(false)}}></ModalChooseScanner>
                    <ResultModal isOpen={resultModal} onClose={() => {setResultModal(false); setIsScanOk(false)}} isOk={isScanOk} patient={patient}></ResultModal>
                </InfiniteScroll>
            </div>
        </>

        // <>
        //
        //     <List bordered={true} loading={isLoading}>
        //         <VirtualList
        //             data={data}
        //             height={CONTAINER_HEIGHT}
        //             itemHeight={50}
        //             itemKey="data"
        //             onScroll={onScroll}
        //         >
        //             {item => (
        //                 <List.Item key={item}>
        //                     <List.Item.Meta
        //
        //                         title={item.fio}
        //                         description={item.ib_num}
        //                     />
        //                     <div><Button color={'cyan'} variant={"solid"} ><ScanOutlined /></Button></div>
        //                 </List.Item>
        //             )}
        //         </VirtualList>
        //     </List>
        //
        // </>
    )
}

export default UserList;