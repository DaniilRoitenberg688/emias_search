import {Divider, List, Skeleton, Spin} from 'antd';
import {Button} from 'antd';
import VirtualList from 'rc-virtual-list';
import {ScanOutlined} from '@ant-design/icons';
import InfiniteScroll from 'react-infinite-scroll-component';

function UserList({data, isLoading, onScroll}) {
    const HEIGHT = window.screen.height
    return (
        <>
            <div id="scrollableDiv"
                 style={{
                     height: '100vh',

                     overflow: 'auto',
                     scrollbarWidth: 0

                 }} >
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
                                  <List.Item.Meta title={item.fio} description={item.ib_num}></List.Item.Meta>
                                  <div>
                                      <Button color={'cyan'} variant={"solid"}><ScanOutlined/></Button>
                                  </div>
                              </List.Item>
                          )} >

                    </List>
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