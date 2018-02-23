const config = {
  content: [
    {
      type: 'row',
      content: [
        {
          type: 'react-component',
          component: 'ChartWithDeepstream',
          title: 'Chart',
          props: { chartName: 'my chart name' },
        },
        // {
        //   type: 'react-component',
        //   component: 'Camera',
        //   title: 'Camera #1',
        //   props: { cameraID: '1' },
        // },
        // {
        //   type: 'react-component',
        //   component: 'RoverApiSettings',
        //   title: 'RoverApiSettings',
        // },
      ],
    },
  ],
};

export default config;
